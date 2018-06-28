ENV["PYTHON"] = "C:\\anaconda\\python.exe"
Pkg.build("PyCall")
using PyCall
using DataFrames
using TextAnalysis
using Dates

inicial_time = Dates.now()

@pyimport pandas
dataset = pandas.read_excel("C:\\Datasets\\Noticias_IC.xlsx")
column = dataset["Classificação"]

nomes = []

for s in dataset
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
while(i <= 240)
    article = []
    article = string(title[i], " ", subtitle[i], " ", news[i])
    i = i + 1
    push!(document, article)
end

i = 1
documento = ""
while(i <= 240)
    documento = string(documento, " ", document[i])
    i = i + 1
end
n_gram = NGramDocument(uppercase(documento))
dict_vocabulary = ngrams(n_gram)
#Now, we are gonna group the DataFrame by Classification

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
    n_gram_grouped = NGramDocument(uppercase(aux))
    push!(dict_grouped, ngrams(n_gram_grouped)) #After that, create each corpus
end

text_test = "Em partida com duas viradas, Guarani-MG goleia Democrata SL Bugre abre o placar, toma a virada, mas volta à frente do placar e vence o lanterna da competição por 6 a 2, no Farião O Guarani-MG não teve piedade do Democrata SL no Farião. Depois de sair à frente no placar, o Bugre chegou a tomar a virada. Mas quando voltou à frente passou o carro. Vitória por 6 a 2 sobre o Jacaré na tarde deste sábado, no Farião, em Divinópolis, pela 4ª rodada do Módulo II do Campeonato Mineiro. Leomir, duas vezes, Eduardo Mancha, Pedro Felipe, Diego Silva e Ricardo Luz marcaram os gols do Guarani-MG. Vander fez os dois do Democrata SL. O Bugre se recupera da derrota na última rodad e chega aos nove pontos na tabela. O Democrata SL segue com um ponto, na lanterna da competição. Na próxima rodada, o Guarani-MG vai a Uberlândia enfrentar o CAP. A partida está marcada para o sábado, dias 10, às 16h. O Democrata SL joga em casa contra o Social, às 10h de domingo, dia 11."

test_set = pandas.read_excel("C:\\Flask\\pandas_simple.xlsx")

@show("Cheguei no teste")

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

#Calculating the posterior probability, based in the likelihood and the prior one
copia = []
predictions = []
for row in eachrow(dataframe_noticias_test_set)
    aux = ""
    aux = string(aux, " ", row[:Titulo], " ", row[:SubTitulo], " ", row[:Noticia])
    ng_test = NGramDocument(uppercase(aux))
    dict_test = ngrams(ng_test)

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
        i = 1
        while(i <= 6)
            counter = 0
            word_count = 0
            for value in values(dict_grouped[i])
                counter = counter + value
            end
            if(haskey(dict_grouped[i], key))
                word_count = dict_grouped[i][key]
            end
            likelihood[i] = Float64(likelihood[i]*((word_count + 1)/(counter + 21089)))
            likelihood[i] = likelihood[i] * 5000
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
