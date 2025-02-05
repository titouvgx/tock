---
title: Bot intégré
---

# Développer en mode Tock Bot intégré

Le mode _Bot intégré_ Tock permet de développer un bot en utilisant un 
[Domain Specifique Language (DSL)](https://fr.wikipedia.org/wiki/Langage_d%C3%A9di%C3%A9) 
 en [Kotlin](https://kotlinlang.org/).

Contrairement au mode _Bot API_ encore en développement, le _Bot Framework_ Kotlin permet d'exploiter toutes les 
possibilités de la plateforme Tock, notamment :

* Gestion des contextes utilisateurs
* Historique de conversation
* Notions avancées comme la _fusion d'entités_
* Etc.

> Exemple de _fusion d'entités_ : lorsque un utilisateur demande "demain" dans une phrase 
>(appelons cette entité _date_) puis "plutôt le soir" dans une phrase suivante, la fusion permet de mettre à jour 
>automatiquement l'entité (_date_) avec les deux informations complémentaires : jour et créneau horaire dans cet exemple.

Attention : dans ce mode de développement, contrairement au mode [_Bot API_](bot-api.md), il est nécessaire que le module bot 
 dispose d'une connexion à la base de donnée (MongoDB) de la plateforme Tock utilisée.

> Pour appréhender complètement ce qui va suivre, il est recommandé de maîtriser les bases du 
>langage de programmation [Kotlin](https://kotlinlang.org/).

## Démarrer avec le framework

### Documentation KDoc

La documentation du framework au format KDoc est disponible [ici](https://doc.tock.ai/tock/dokka/tock).

### Dépendance `bot-toolkit`

Pour utiliser le framework conversationnel, il faut ajouter la dépendance `bot-tookit` à l'application / au projet
Kotlin.

Par exemple dans un projet [Maven](https://maven.apache.org/) :

```xml
        <dependency>
            <groupId>ai.tock</groupId>
            <artifactId>bot-toolkit</artifactId>
            <version>24.9.6</version>
        </dependency>
```

Ou dans un projet [Gradle](https://gradle.org/) :

```groovy
      compile 'ai.tock:bot-toolkit:24.9.4'
```

### Un bot est un ensemble de parcours (stories)

Voici par exemple comment le Bot Open Data est défini :

```kotlin
val openBot = bot(
        "bot_open_data",
        stories =
        listOf(
                greetings,
                departures,
                arrivals,
                search
        ),
        hello = greetings
)
```

Ce bot comporte un identifiant (obligatoire - "bot_open_data") et une liste de parcours ou _stories_.
 
Une _Story_ est un regroupement fonctionnel qui correspond à une intention principale et, de manière optionelle,
à une ou plusieurs intentions dites "secondaires" (voir [Concepts](../user/concepts.md)).

Ici le bot définit 4 parcours : `greetings`, `departures`, `arrivals` et `search`. 

Le parcours `greetings` est déclaré comme parcours principal, il sera présenté par défaut au début d'une conversation :
`hello = greetings`.

### Une Story simple 

_Comment définit-on une Story?_

Voici une première version simplifiée du parcours `greetings` :

```kotlin
val greetings = story("greetings") {
    send("Bienvenue chez le Bot Open Data Sncf! :)")
    end("Il s'agit d'un bot de démonstration du framework Tock : https://github.com/theopenconversationkit/tock")
}
```

Notez que dans le corps de la fonction, `this` est de type [`BotBus`](https://doc.tock.ai/tock/dokka/tock/ai.tock.bot.engine/-bot-bus/index.html),
à partir duquel vous pouvez interagir avec l'utilisateur, et qui permet également d'accèder
à tous les élements contextuels disponibles.

Concrètement sela signifie que quand l'intention `greetings` sera détectée par le modèle NLP, la fonction ci-dessus sera appelée par le framework Tock.

Le bot envoie donc successivement une première phrase de réponse (`bus.send()`), puis un deuxième en indiquant que c'est 
la dernière phrase de sa réponse à l'aide d'un `bus.end()`.

Voici maintenant la version complète de `greetings` :

```kotlin
val greetings = story("greetings") {
    //cleanup state
    resetDialogState()

    send("Bienvenue chez le Bot Open Data Sncf! :)")
    send("Il s'agit d'un bot de démonstration du framework Tock : https://github.com/theopenconversationkit/tock")

    withMessenger {
        buttonsTemplate(
              "Il est volontairement très limité, mais demandez lui un itinéraire ou les départs à partir d'une gare et constatez le résultat! :) ",
              postbackButton("Itinéraires", search),
              postbackButton("Départs", Departures),
              postbackButton("Arrivées", Arrivals)
        )
    }
    withGoogleAssistant {
       gaMessage(
              "Il est volontairement très limité, mais demandez lui un itinéraire ou les départs à partir d'une gare et constatez le résultat! :) ",
              "Itinéraires",
              "Départs",
              "Arrivées")
       }

    end()
}
``` 

Deux notions ont été ajoutées :

- `resetDialogState()` qui permet de repartir d'un contexte utilisateur vide (en oubliant les éventuels échanges précédents)

- les méthodes `withMessenger{}` et `withGoogleAssistant{}` qui permettent de définir des réponses spécifiques pour chaque connecteur.
Ici un texte avec des boutons pour Messenger, et un texte avec des suggestions pour Google Assistant.

### Démarrer et connecter le bot

Pour démarrer le bot, il suffit de rajouter dans votre `main` principal l'appel suivant :

```kotlin
registerAndInstallBot(openBot)
``` 

La variable `openBot` dans l'exemple est le bot que vous avez défini plus haut.

Une fois le bot démarré, il est également nécessaire de spécifier quels connecteurs sont utilisés
dans l'interface d'administration du bot, du menu _Configuration_ > _Bot Configurations_ > _Create a new configuration_.

Pour en savoir plus sur les différents canaux et connecteurs, voir [cette page](../user/guides/canaux.md).

### Importer la configuration (dumps)

Il est possible d'exporter différentes configurations depuis Tock Studio, puis les
importer automatiquement au démarrage du bot.

Une fois exportés les fichiers _dumps_ de Tock Studio dans le _classpath_ du bot, 
on peut appeler une ou plusieurs des fonctions suivantes depuis le `main` :

* `importApplicationDump` : importe une application à partir d'un 
  [_dump_ d'application](../user/studio/configuration.md#modifier-importer-et-exporter-une-application).
  Remarque : l'import est ignoré si l'application cible existe déjà.
* `importNlpDump` : importe un modèle NLP (intentions, phrases, entités) à partir d'un
  [_dump_ NLP](../user/studio/configuration.md#modifier-importer-et-exporter-une-application).
* `importI18nDump` : importe des labels (aka _i18n_) à partir d'un
  [_dump_ de labels](../user/studio/stories-and-answers.md#longlet-answers).

Exemple :

```kotlin
fun main(args: Array<String>) {

  registerAndInstallBot(bot)

  // Import application
  importApplicationDump("/bot_app_dump.json")

  // Import NLP model (intents, sentences, entities...)
  importNlpDump("/bot_nlp_dump.json")
  
  // Import story labels (aka i18n)
  importI18nDump("/bot_labels_dump.json")
}
```

## Aller plus loin

Bien sûr, le `StoryHandler` de `greetings` ne dépend pas du contexte : la réponse est toujours la même.
 
Pour le développement de stories complexes, nous avons besoin d'une abstraction supplémentaire.

### Intentions secondaires

Voici le début de la définition de la story `search` :

```kotlin
val search = storyDef<SearchDef>(
        "search",
        otherStarterIntents = setOf(indicate_origin),
        secondaryIntents = setOf(indicate_location)) {
   
}
``` 

Le parcours `search` définit une intention secondaire "de démarrage" (`indicate_origin`) 
et une intention secondaire simple (`indicate_location`).

Une intention secondaire "de démarrage" est semblable en tout point à une intention principale : 
dès que cette intention est détectée, le parcours `search` va être exécuté, 
si la story courante ne possède pas cette intention en tant qu'intention secondaire.

Pour une intention secondaire simple, par contre, la story ne sera exécutée que si la story courante du contexte 
est "déjà" la story search. Plusieurs story différentes peuvent donc partager les mêmes intentions secondaires.

### Manipuler les entités

Pour récupérer les valeurs des entités, une bonne pratique est de définir des **extensions**. 
Par exemple voici le code utilisé pour récupérer l'entité `destination` :

```kotlin

val destinationEntity = openBot.entity("location", "destination") 

var BotBus.destination: Place?
    get() = place(destinationEntity)
    set(value) = setPlace(destinationEntity, value)
    
private fun BotBus.place(entity: Entity): Place? = entityValue(entity, ::placeValue)?.place

private fun BotBus.setPlace(entity: Entity, place: Place?) = changeEntityValue(entity, place?.let { PlaceValue(place) })
    
```

Une entité de type `location` et de role `destination` est créée. 
Il s'agit de l'entité correspondante dans le modèle NLP.

Une variable `destination` est définie, qui va simplifier la manipulation de cette entité dans le code métier.
Cette variable contient la valeur actuelle de la destination dans le contexte utilisateur.

Voici une version complétée de la story `search` qui utilise `destination` :

```kotlin

val search = storyDef<SearchDef>(
        "search",
        setOf(indicate_origin),
        setOf(indicate_location)) {

        //check mandatory entities
        when {
            destination == null -> end("Pour quelle destination?")
            origin == null -> end("Pour quelle origine?")
            departureDate == null -> end("Quand souhaitez-vous partir?")
        } 
}

``` 

Si il n'y a pas de valeur dans le contexte courant pour la destination, le bot demande de spécifier la destination et en reste là.
Idem pour l'origine ou la date de départ.

Si les 3 valeurs obligatoires sont spécifiées, il passe à la réponse proprement dite développée dans la classe (`SearchDef`).

La version complète de cette première partie du code est la suivante :

```kotlin

val search = storyDef<SearchDef>(
        "search",
        setOf(indicate_origin),
        setOf(indicate_location)) {

        //handle generic location intent
        if (isIntent(indicate_location) && location != null) {
            if (destination == null || origin != null) {
                destination = returnsAndRemoveLocation()
            } else {
                origin = returnsAndRemoveLocation()
            }
        }    
    
        //check mandatory entities
        when {
            destination == null -> end("Pour quelle destination?")
            origin == null -> end("Pour quelle origine?")
            departureDate == null -> end("Quand souhaitez-vous partir?")
        }
}

```

Dans le cas où l'intention détectée est `indicate_location`, nous ne savons pas si la localité indiquée représente l'origine ou la destination.
Il est donc codé une règle simple : 
Si il existe déjà dans le contexte une origine et pas de destination, la nouvelle localité est en fait la destination.
Sinon, il s'agit de l'origine. 

### Utiliser `HandlerDef`

Dans la définition de la story `search` ci-dessus, vous avez pu noter le typage générique `SearchDef`. 
Voici le code de cette classe :

```kotlin
@GAHandler(GASearchConnector::class)
@MessengerHandler(MessengerSearchConnector::class)
class SearchDef(bus: BotBus) : HandlerDef<SearchConnector>(bus) {
   
    private val d: Place = bus.destination!!
    private val o: Place = bus.origin!!
    private val date: LocalDateTime = bus.departureDate!!

    override fun answer() {
        send("De {0} à {1}", o, d)
        send("Départ le {0}", date by datetimeFormat)
        val journeys = SncfOpenDataClient.journey(o, d, date)
        if (journeys.isEmpty()) {
            end("Désolé, aucun itinéraire trouvé :(")
        } else {
            send("Voici la première proposition :")
            connector?.sendFirstJourney(journeys.first())
            end()
        }
    }
}
```

`SearchDef` étend `HandlerDef` qui est un alias d'une classe du framework Tock.

C'est en général ici que l'on va définir le code métier des parcours complexes. 

Le code est relativement parlant, mais il contient une abstraction supplémentaire : `SearchConnector`.

`SearchConnector` est la classe qui définit le comportement spécifique à chaque connecteur, et les annotations
 `@GAHandler(GASearchConnector::class)` et `@MessengerHandler(MessengerSearchConnector::class)` 
 indiquent les implémentations correspondantes pour les différents connecteurs supportés (respectivement Google Assistant et Messenger).
 
 Que se passerait-il s'il n'y avait pas de connecteur pour Google Assistant par exemple ? 
 La méthode `connector?.sendFirstJourney(journeys.first())` n'enverrait pas la réponse finale, puisque `connector` serait `null`.
 
### Utiliser `ConnectorDef`

Voici maintenant une version simplifiée de `SearchConnector` :

```kotlin
sealed class SearchConnector(context: SearchDef) : ConnectorDef<SearchDef>(context) {

    fun Section.title(): CharSequence = i18n("{0} - {1}", from, to)

    fun sendFirstJourney(journey: Journey) = withMessage(sendFirstJourney(journey.publicTransportSections()))
    
    abstract fun sendFirstJourney(sections: List<Section>): ConnectorMessage

}
``` 

Et voici son implémentation pour Messenger :

```kotlin
class MessengerSearchConnector(context: SearchDef) : SearchConnector(context) {

    override fun sendFirstJourney(sections: List<Section>): ConnectorMessage =
          flexibleListTemplate(
                sections.map { section ->
                      with(section) {
                          listElement(
                                title(),
                                content(),
                                trainImage
                          )
                      }
                },
                compact
          )
}
```

Le code spécifique à chaque connecteur est ainsi correctement découplé. Le code commun à chaque connecteur est présent dans `SearchConnector` et le comportement spécifique à
chaque connecteur se trouve dans les classes dédiées.

### Utiliser `StoryStep`

Parfois il est nécessaire de se souvenir de l'étape à laquelle l'utilisateur se trouve
dans la story courante. Pour cela Tock met à disposition la notion de `StoryStep`.

Il existe deux types de `StoryStep` :

#### `SimpleStoryStep`

A utiliser dans les cas simples, pour lequels on va gérer le comportement induit directement :

```kotlin
enum class MyStep : SimpleStoryStep { a, b }

val story = storyWithSteps<MyStep>("intent") {
    if(step == a) {
        // ...
    } else if(step == b) {
        // ...
    } else {
        //default case
    }
}
```

Pour modifier l'étape courante, deux méthodes sont disponibles :

* Modifier manuellement l'étape

```kotlin
val story = storyWithSteps<MyStep>("intent") {
    //(...)
    step = MyStep.a
    // l'étape sera persistée tant que nous resterons dans cette story
}
```

* Utiliser les boutons ou autres _quick replies_

Plus de détails sur ce sujet [plus bas](#postback-buttons-quick-replies).

#### Les `StoryStep` avec comportement

Dans des cas plus complexes, on souhaite pouvoir définir un comportement pour chaque étape. 
L'utilisation de [`HandlerDef`](#utiliser-handlerdef) est alors un prérequis.

```kotlin
enum class MySteps : StoryStep<MyHandlerDef> {

    //pas de comportement spécifique
    display,

    select {

        // la step "select" sera automatiquement sélectionnée si la sous-intention select est détectée
        override val intent: IntentAware? = SecondaryIntent.select
        //dans ce cas la réponse suivante sera apportée
        override fun answer(): MyHandlerDef.() -> Any? = {
            end("I don't know yet how to select something")
        }
    },

    disruption {
        //seule la réponse est configurée
        override fun answer(): ScoreboardDef.() -> Any? = {
            end("some perturbation")
        }
    };
}
```

Davantage d'options de configuration sont disponibles. Consultez la description de 
[`StoryStep`](https://doc.tock.ai/tock/dokka/tock/ai.tock.bot.definition/-story-step/index.html). 

### *Postback buttons* & *quick replies*

Messenger met à disposition ce type de bouton, et la plupart des connecteurs avec interface graphique font de même.

Tock permet de définir l'action effectuée suite à un clic sur ces boutons. 

Dans l'exemple suivant, le bouton redirigera vers l'intention `search`. 

```kotlin
buttonsTemplate(
            "The bot is very limited! Only itineraries are supported :)",
            postbackButton("Itineraries", search)

```
 
Il est possible de définir également une `StoryStep` et des paramètres dédiés :

```kotlin

//pour définir des paramètres, la pratique recommandée est d'étendre l'interface ParameterKey
enum class ChoiceParameter : ParameterKey {
    nextResultDate, nextResultOrigin
}

buttonsTemplate(
            "The bot is very limited! Only itineraries are supported :)",
            postbackButton(
                "Itineraries",
                intent = search, 
                //si aucune step n'est indiquée, c'est la step courante qui est utilisée
                step = MyStep.a, 
                parameters =  
                    //ce paramètre est stocké sous forme de chaîne de caractère (les crochets sont utilisés)
                    nextResultDate[nextDate] + 
                    //ce paramètre est stocké en json (les parenthèses sont utilisées)
                    nextResultOrigin(origin)
            )

``` 

Pour récupérer les paramètres du bouton sur lequel on a cliqué :

```kotlin
    val isClick = isChoiceAction()
    val nextDate = choice(nextResultDate)
    val nextOrigin : Locality = action.jsonChoice(nextResultOrigin)
```

### Tests Unitaires

La page [Tests Unitaires](test.md) présente le framework fourni pour réaliser des TUs  avec Tock.
