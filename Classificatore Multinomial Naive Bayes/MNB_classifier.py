import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, StratifiedKFold
import pickle
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

dataset = pd.read_csv("Train/data_train.csv")
dataset = dataset[:3102]

target = list(set(dataset['category']))

features = CountVectorizer()
X_tf = features.fit_transform(dataset['full_text'])

with open('../ProgettoAI/flask-app/model/vectorizer.pkl', 'wb') as fid:
    pickle.dump(features, fid)

classifier = MultinomialNB()
categories = list(dataset['category'])

classifier.fit(X_tf, categories)



#data1 = "La prima regione ""stellata"" non c'è. Davide non ce l'ha fatta contro Golia, una sola lista non riesce a travolgerne 9 dello schieramento avversario. Così il M5s non replica fino in fondo l'onda del 4 marzo e il Molise va al centrodestra, e al suo candidato governatore, il sessantenne commercialista di Fi DonatoToma. Quando mancano un paio di sezioni alla fine dello scrutinio , Toma è al 43,6 per cento (circa 64mila voti) contro il 38,5 (circa 55mila consensi) di Andrea Greco, il 33enne avvocato lanciato da Di Maio. Terzo, come previsto ampiamente, l'aspirante governatore del centrosinistra, Carlo Veneziale del Pd, che con la coaliziome unitaria non riesce ad andare oltre il 17 (circa 24mila). Ma un primato resta e forse peserà ancora: il partito fondato da Grillo e Casaleggio, nonostante il calo netto rispetto alla quota record del 45 per cento del 4 marzo, arriva in Molise al 31 per cento, cioè oltre tre volte più di Forza Italia (9,48), quasi 4 volte la misura della Lega (8,26), e del Pd (8,9). ELEZIONI IN MOLISE, LO SPOGLIO IN DIRETTA ""Incidenze su Roma? Noi non abbiamo ricette - dice il vincitore - ma certamente abbiamo una ricetta per governare il Molise, lo faremo senza incertezze, dando stabilità"", riconoscendo il vantaggio di una legge elettorale - nuova di zecca, varata dalla giunta uscente di centrosinistra guidata da Paolo Frattura - senza voto disgiunto, un sistema proporzionale a turno unico che assegna un premio di maggioranza del 60 per cento secco a chi porta a casa un voto in più. ""Le prime mosse? Subito la ricognizione della situazione debitoria della Regione Molise per accelerare i pagamenti alle imprese e avviare quella semplificazione di cui il territorio ha bisogno per ripartire"". Quanto alle divisioni interne e ai trasformismi che potrebbero minare l'apparente coesione dello schieramento vincente, Toma sembra sereno: ""Gli elettori ci hanno premiato, ora dobbiamo governare e mettercela tutta. Garantisco che sarò il presidente di tutti"". E Berlusconi salta subito sulla vittoria per rivendicare la guida del governo e attaccare di nuovo il M5s: ""Dal Molise parte un segnale nazionale importante: il centrodestra unito ha la capacità di raccogliere il consenso degli italiani per guidare le regioni ed il Paese. Il messaggio degli elettori è stato chiaro, ora dobbiamo impegnarci con tutte le nostre energie per ripetere lo stesso successo in Friuli"". Dal Cavaliere arriva anche una stoccata, l'ennesima, al M5S. ""Dal Molise - scrive infatti l'ex premier - però esce anche battuto e fortemente ridimensionato il dilettantismo dei Cinque Stelle, rispetto al voto di protesta espresso dagli elettori alle politiche. I grillini si confermano del tutto non credibili per una funzione di governo"". Ancora più esplicita Giorgia Meloni che rivendica l'exploit di Fratelli d'Italia, unico partito in crescita rispetto alle politiche: ""Il risultato è una indicazioone chiara per il Quirinale: gli italiani vogliono un governo di centrodestra con un programma di centrodestra""."
#data2 = "Tragedia stamane in un supermercato all'ingrosso della catena Metro di Elmas, centro alle porte di Cagliari, dove una bimba di neanche due anni è morta schiacciata dalla merce esposta caduta da uno scaffale sul passeggino spinto dalla madre. Secondo i primi accertamenti effettuati dai carabinieri la merce che ha travolto la piccola è caduta da un'altezza considerevole a causa della rottura di uno dei sostegni dello scaffale. Era presenta anche il padre della bimba ma sia lui che la madre sono rimasti illesi. Genitori e parenti distrutti dal dolore, in lacrime nel descrive l'episodio: ""La piccola era la cosa più bella che avevamo e Sofia ora non c'è più"". Imprevedibile la morte di Sofia Saddi, che a dicembre avrebbe compiuto due anni, schiacciata da un carico di involucri per pizze, mentre si trovava in un negozio all'ingrosso con il padre Alessio e la madre Valentina. La tragedia è avvenuta alle 14 nel centro ""Metro"", nella zona industriale di Elmas, alle porte di Cagliari. Padre, madre e figlia, quest'ultima seduta su un passeggino come previsto dal regolamento del centro commerciale affisso sulle porte d'ingresso, giravano fra le varie corsie, forse cercavano alcuni prodotti per il bar che il padre gestisce a Sinnai (Cagliari). Si sono fermati in quella dove c'erano gli involucri di cartone. Forse a causa della rottura di un perno dell'alta scaffalatura o per ragioni ancora non accertate, una pedana su cui erano poggiati circa 300 kg di imballaggi di cartone si è sganciata e il bancale è scivolato. La piccola è stata travolta dal ""macigno"", sotto gli occhi impotenti dei genitori. Il peso ha schiacciato il passeggino, tanto che le ruote si sono piegate. I genitori e gli addetti del centro sono subito intervenuti per soccorrerla. La bambina è stata trasportata vicino alle casse del negozio mentre a Elmas è arrivata un'ambulanza del 118, ma nonostante l'intervento tempestivo dei medici, per la piccola Sofia non c'è stato nulla da fare. Sul posto son arrivati i carabinieri della Compagnia di Cagliari e della Stazione di Sant'Avendrace che hanno avviato le indagini. Il pm di turno, Andrea Massidda, ha disposto il sequestro della corsia teatro della tragedia. La Procura, che ha aperto un fascicolo al momento senza nessun indagato, intende accertare nel dettaglio cosa è accaduto, ricostruire l'incidente. Non è escluso che venga nominato anche un consulente. ""Era un involucro pesantissimo - racconta disperato il nonno della piccola Sofia, arrivato subito sul posto - la bambina era la cosa più bella che avevamo. La mamma si è sentita male, è incinta, l'hanno portata in ospedale"". Nessuno degli addetti o dei responsabili della Metro ha voluto rilasciare dichiarazioni. Sulla porta è stato affisso cun cartello: ""Il punto vendita rimarrà chiuso per un paio di giorni""."
#data3 = "Una tigre fuggita dallo zoo di Tbilisi ha ucciso un uomo nel centro della città. La tigre è stata abbattuta dalla polizia georgiana. L'animale - inizialmente scambiato per un leone dai media locali - era fuggito dallo zoo della capitale georgiana assieme a molti altri esemplari dopo le inondazioni che pochi giorni fa ha ucciso almeno 19 persone. La belva, una tigre albina, si nascondeva in una fabbrica abbandonata. L'amministrazione dello zoo aveva annunciato ieri che nell'inondazione erano morti 8 leoni, 7 tigri, almeno 2 giaguari su 3 e 12 orsi su 14. Le strade della città sono ancora impraticabili dopo che il fiume Vere, che costeggia lo zoo della città, è esondato in seguito alle piogge torrenziali causando 19 morti. Molti animali sono fuggiti, mentre almeno 300 sono annegati. Mancano ancora all'appello due tigri, un orso e uno sciacallo ha detto Ivane Darazelia, veterinaria dello zoo. I danni sono stati conteggiati in 13 milioni di euro, secondo il ministero delle Finanze georgiano. Il premier georgiano, Irakli Garibashvili , ha già invitato la popolazione a non lasciare le abitazioni fino a quando le bestie non saranno catturate. Per farlo, il ministro dell'Interno ha mobilitato anche le forze speciali. Le piogge sono iniziate nella serata di sabato e in poche ore il fiume Vera, che scorre in mezzo a Tbilisi, è straripato: molte persone risultano ancora disperse. Migliaia sono rimaste senza corrente elettrica e senza acqua, mentre altre sono state tratte in salvo con l'aiuto degli elicotteri. Il sindaco di Tbilisi, Davit Narmania , ha riferito che la situazione è ""molto grave"". Georgia, inondazione a Tbilisi: animali in fuga dallo zoo"

#test_data = [data1, data2, data3]

#test_msg_counts = features.transform(test_data)

#classifications = classifier.predict(test_msg_counts)
#print(classifications)

#scores = cross_val_score(classifier, X_tf, categories, cv=5)
scores = cross_val_score(classifier, X_tf, categories, cv=StratifiedKFold(10), scoring="accuracy")
#scores = cross_val_score(classifier, X_tf, categories, cv=10, scoring="accuracy")

#scores = cross_val_predict(classifier, X_tf, categories, cv=StratifiedKFold(10))
#cm = confusion_matrix(categories, scores, target)

#disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=target)
#disp.plot(cmap=plt.cm.Blues, xticks_rotation=90)

#plt.show()  

with open('../ProgettoAI/flask-app/model/estimator.pkl', 'wb') as fid:
    pickle.dump(classifier, fid)

# Print the accuracy of each fold:
i = 1
for score in scores:
    print("Iterazione",i,": Percentuale di accuratezza = ",round(score*100,2),"%")
    i+=1

# Print the mean accuracy of all 10 folds
print("Percentuale media di accuratezza:",round(scores.mean()*100,2),"%")
