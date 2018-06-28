ENV["PYTHON"] = "C:\\anaconda\\python.exe"
Pkg.build("PyCall")
using PyCall
using DataFrames
using TextAnalysis
using Dates

inicial_time = Dates.now()

@pyimport pandas
dataset = pandas.read_excel("C:\\Datasets\\Noticias_IC_Menos_25.xlsx")
column = dataset["Classificação"]


nomes = []

for s in dataset
    @show s
    push!(nomes, s)
end

#Setting each column of the dataset for futher transformation at a Julia DataFrame
url = []
title = []
subtitle = []
news = []
classication = []
i = 1

for name in nomes
    column = dataset[name]
    info = []

    for text in column
        push!(info, text)
    end

    if(i == 1)
        url = copy(info)

    elseif(i == 2)
        title = copy(info)

    elseif(i == 3)
        subtitle = copy(info)

    elseif(i == 4)
        news = copy(info)

    elseif(i == 5)
        classication = copy(info)
    end
    i = i + 1

end

#Creating a Julia DataFrame, for futher use
dataframe_noticias = DataFrame(
Titulo = title,
SubTitulo = subtitle,
Noticia = news,
Classificacao = classication)

document = []
#Creating the corpus
i = 1
while(i <= 90)
    article = []
    article = string(title[i], " ", subtitle[i], " ", news[i])
    i = i + 1
    push!(document, article)
end

i = 1
documento = ""
while(i <= 90)
    documento = string(documento, " ", document[i])
    i = i + 1
end
sd = StringDocument(uppercase(documento))
dict_vocabulary = ngrams(sd, 3)

#Creating the corpus of each news category
grouped_noticias = groupby(dataframe_noticias, [:Classificacao]) #First, we need to aggrupate them
dict_grouped = []
classes = []
for group in grouped_noticias
    aux = ""
    push!(classes, Dict(group[:Classificacao][1] => nrow(group)))
    for row in eachrow(group)
        aux = string(aux, " ", row[:Titulo], " ", row[:SubTitulo], " ", row[:Noticia])
    end
    sd_grouped = StringDocument(uppercase(aux))
    push!(dict_grouped, ngrams(sd_grouped, 3)) #After that, create each corpus
end

#It can be seen that the many bigrams had unnecessary punctuations on it, even have a single word (Probably because of paragraphs' end)
#So, when the program will take analyze the words, the treatment will be necessary

test_set = pandas.read_excel("C:\\Flask\\pandas_simple1.xlsx")

url = []
title = []
subtitle = []
news = []
classication = []
i = 1

for name in nomes
    column = test_set[name]
    info = []

    for text in column
        push!(info, text)
    end

    if(i == 1)
        url = copy(info)

    elseif(i == 2)
        title = copy(info)

    elseif(i == 3)
        subtitle = copy(info)

    elseif(i == 4)
        news = copy(info)

    elseif(i == 5)
        classication = copy(info)
    end
    i = i + 1

end

#Creating a Julia DataFrame, for futher use
dataframe_noticias_test_set = DataFrame(
Titulo = title,
SubTitulo = subtitle,
Noticia = news,
Classificacao = classication)

copia = []
predictions = []
char_to_take_out = ['.', ',', '!', '?', '+', '*', '/', ':', ';', '(', ')','"']
io_principal = IOBuffer()
io_secundary = IOBuffer()

for row in eachrow(dataframe_noticias_test_set)
    aux = ""
    aux = string(aux, " ", row[:Titulo], " ", row[:SubTitulo], " ", row[:Noticia])
    sd_test = StringDocument(uppercase(aux))
    dict_test = ngrams(sd_test, 3)

    #Calculating the prior probability (Considering only the numbers of occurrences of each category)
    prior = []
    i = 1
    while(i <= 6)
        for key in keys(classes[i])
            result = (classes[i][key])/(nrow(dataframe_noticias))
            push!(prior, result)
        end
        i = i + 1
    end

    likelihood = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    for key in keys(dict_test)
        #Now, we should treat the keys of the dictionary
        for char in key
            if char in char_to_take_out

            else
                write(io_principal, char)
            end
        end
        trigram_treated = String(take!(io_principal))
        trigrams_names = split(trigram_treated)
        number_words = length(trigrams_names)
        i = 1
        while(i <= 6)
            counter = 0 #Number of occurrences that the first bigram of the trigram appears as a first bigram in another trigrams
            trigram_count = 0 #Number of occurtences that this trigram appears in the corpus of the category
            if(haskey(dict_grouped[i], key))
                trigram_count = dict_grouped[i][key] #Even if the trigram is just a word or a bigram, we still count like this
            end
            if(number_words == 3) #Here, we should check how many trigrams start with the first bigram of the current trigram at analysis
                for secundary_key in keys(dict_grouped[i])

                    secundary_trigrams_names = []
                    if(contains(secundary_key, " "))
                        secundary_trigrams_names = split(secundary_key)
                    else
                        push!(secundary_trigrams_names, secundary_key)
                        push!(secundary_trigrams_names,"0")
                        push!(secundary_trigrams_names,"0")
                    end

                    if(contains(secundary_trigrams_names[1], trigrams_names[1]) && contains(secundary_trigrams_names[2], trigrams_names[2]))
                        counter = counter + dict_grouped[i][secundary_key]
                    end

                end
            elseif(number_words == 2) #Here, we should check how many bigrams will count
                for secundary_key in keys(dict_grouped[i])
                    secundary_trigrams_names = []
                    if(contains(secundary_key, " "))
                        secundary_trigrams_names = split(secundary_key)
                    else
                        push!(secundary_trigrams_names, secundary_key)
                        push!(secundary_trigrams_names,"0")

                    end

                    if(contains(secundary_trigrams_names[1], trigrams_names[1]))
                        counter = counter + dict_grouped[i][secundary_key]
                    end
                end
            elseif(number_words == 1)
                for value in values(dict_grouped[i])
                    counter = counter + value
                end
            end
            likelihood[i] = Float64(likelihood[i]*((trigram_count + 1)/(counter + 82344)))
            likelihood[i] = likelihood[i] * 60000


            i = i + 1
        end
    end
    outcomes = []
    i = 1
    while(i <= 6)
        push!(outcomes, prior[i]*likelihood[i])
        i = i + 1
    end

    answer = ""
    max = outcomes[1]
    i = 1
    while(i <= 6)
        for key in keys(classes[i])
            if(outcomes[i] >= max)
                answer = key
                max = outcomes[i]
            end
        end
        i = i + 1
    end
    push!(predictions, answer)
    push!(copia, outcomes)
end

@pyimport sklearn.metrics as skc

accuracy = skc.accuracy_score(classication, predictions)
cm = skc.confusion_matrix(classication, predictions)
cohen_kappa = skc.cohen_kappa_score(classication, predictions)

final_time = Dates.now()

@show(final_time - inicial_time)
