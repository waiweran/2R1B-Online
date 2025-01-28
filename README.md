# Description
Online implementation of 2 Rooms and a Boom by Tuesday Knight Games
Free print and play version

# Website
[http:](http://tworooms.net)

## Server Notes
To update, copy files then restart

# Setup Requirements
The rule book and character guide from the print and play (saved as RuleBook.pdf and CharacterGuide.pdf) should be included in the static folder.
### Images
Card images should be included in static/Cards, named in CamelCase by card name preceeded by team if needed to differentiate images (ex. Bomber.png, RedAgent.png). 
Team images (portion of card for team sharing) should be included in static/Teams. Team images include RedTeam.png, BlueTeam.png, GrayTeam.png, GreenTeam.png (leprechaun), ZombieTeam.png, and UnknownTeam.png (drunk).
A partially clear Zombie overlay image to indicate an infected player should be added to static/Cards and static/Teams, both ZombieOverlay.png, both the same size as the other images in their respective folder.
Character descriptions from the character guide are included in static/Characters as images, named by ID number in Cards.py and game.js (ex. 0.png, 1.png, 2.png etc.) with the exception of the President and Bomber descriptions, which are included as PresidentBomber.png
### Javascript Libraries
The Dragula javascript library should be included in the static folder.
