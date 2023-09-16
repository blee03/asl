import pygame
import sys
import random
import time

#a list of enemies per region, 1-3 are regular enemies, 4 is the boss
enemies_dict_forest = {1: "Fairy", 2: "Wolf", 3: "Goblin", 4: "Ogre"}
enemies_dict_desert = {1: "Snake", 2: "Scorpion", 3: "Goblin", 4: "Mummy Queen"}
enemies_dict_dungeon = {1: "Skeleton", 2: "Goblin", 3: "Ghost", 4: "Lich"}
enemies_dict_hell = {1: "Demon", 2: "Goblin", 3: "Ghost", 4: "Devil"}
enemies_dict_castle = {1: "Knight", 2: "Goblin", 3: "Wizard", 4: "Dragon"}
enemies_dict_lake = {1: "Fairy", 2: "Sahuagin", 3: "Goblin", 4: "Kraken"}

#the list of regions
regions_dict = {"Forest":enemies_dict_forest, "Desert":enemies_dict_desert, "Dungeon":enemies_dict_dungeon, "Hell":enemies_dict_hell, "Castle":enemies_dict_castle, "Lake":enemies_dict_lake}
#the images for each region, which will be used as the background
regions_images = {"Forest":pygame.image.load("forest.png"), "Desert":pygame.image.load("desert.png"), "Dungeon":pygame.image.load("dungeon.png"), "Hell":pygame.image.load("hell.png"), "Castle":pygame.image.load("castle.png"), "Lake":pygame.image.load("lake.png")}
#the images for each enemy
enemies_images = {"Fairy":pygame.image.load("fairy.png"), "Wolf":pygame.image.load("wolf.png"), "Goblin":pygame.image.load("goblin.png"), "Ogre":pygame.image.load("ogre.png"), "Snake":pygame.image.load("snake.png"), 
                  "Scorpion":pygame.image.load("scorpion.png"), "Mummy Queen":pygame.image.load("mummy_queen.png"), "Skeleton":pygame.image.load("skeleton.png"), "Ghost":pygame.image.load("ghost.png"), "Lich":pygame.image.load("lich.png"), 
                  "Demon":pygame.image.load("demon.png"), "Devil":pygame.image.load("devil.png"), "Knight":pygame.image.load("knight.png"), "Wizard":pygame.image.load("wizard.png"), 
                  "Dragon":pygame.image.load("dragon.png"), "Kraken":pygame.image.load("kraken.png"), "Sahuagin":pygame.image.load("sahuagin.png")}
#defines the properties of an enemy
class enemy:
    def __init__(self,stage,zone):
        self.health = (random.randint(1,10)*stage) #the health of the enemy, scales with stage
        self.type = regions_dict[zone][random.randint(1,3)] #the type of enemy, chosen randomly from the list of enemies in the region

    def take_damage(self, damage):
        self.health -= damage
    def make_boss(self,zone):
        self.health = 20*stage
        self.type = regions_dict[zone][4]
    
    def get_health(self):
        return self.health
    def get_type(self):
        return self.type
    
    def is_dead(self) -> bool:
        if self.health <= 0:
            return True
        else:
            return False
#defines the properties of a stage
class stage:
    def __init__(self, stage_num, zone):
        self.stage_num = stage_num
        self.enemy_list = [] #contains the health values for each enemy
        for i in range(0,9):
            self.enemy_list.append(enemy(stage_num, zone))
        boss = enemy(stage_num, zone)
        boss.make_boss(zone)
        self.enemy_list.append(boss)
    #return the list of enemies
    def get_enemy_list(self):
        return self.enemy_list
    #return the stage number
    def get_stage_num(self):
        return self.stage_num
    #determine if the stage is complete
    def is_stage_complete(self) -> bool:
        if len(self.enemy_list) == 0:
            return True
        else:
            return False
    #return the current enemy, which should be the first enemy in the list    
    def get_current_enemy(self):
        return self.enemy_list[0]
    #when the current enemy is killed, remove it from the list
    def kill_current_enemy(self):
        self.enemy_list.pop(0)
    #return the number of enemies remaining in the stage
    def get_num_enemies(self):
        return len(self.enemy_list)
    
#defines the properties of the player
class player:
    def __init__(self):
        self.health = 50
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.crit_multiplier = 1
        self.damage_multiplier = 1
    #getters for player properities
    def get_health(self):
        return self.health
    def get_level(self):
        return self.level
    def get_exp(self):
        return self.exp
    def get_gold(self):
        return self.gold
    def get_crit_multiplier(self):
        return self.crit_multiplier
    def get_damage_multiplier(self):
        return self.damage_multiplier
    #deal damage to the player when they fail to make a move
    def take_damage(self, damage):
        self.health -= damage
    #calculate the damage dealt to an enemy, crit comes from going fast
    def deal_damage(self, enemy, is_crit):
        enemy.take_damage(random.randint(1,3)*self.level*self.damage_multiplier + is_crit*self.crit_multiplier(random.randint(1,3)*self.level))
    #gain exp from killing an enemy
    def gain_exp(self, exp):
        self.exp += exp
        if self.exp % 10 == 0:
            self.level_up()
        self.exp = self.exp % 10
    #gain gold from killing an enemy
    def gain_gold(self, gold):
        self.gold += gold
    #level up the player
    def level_up(self):
        self.level += 1
    #determine if the player is dead
    def is_dead(self) -> bool:
        if self.health <= 0:
            return True
        else:
            return False
    #upgrade the player's stats with gold
    def upgrade_crit(self):
        self.crit_multiplier += 0.2
    def upgrade_damage(self):
        self.damage_multiplier += 0.2
    def restore_health(self):
        self.health += 10
        if self.health > 50:
            self.health = 50
    #spend gold to buy upgrades
    def spend_gold(self, amount):
        self.gold -= amount
#handles the game logic
class game_runner:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800,600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        self.player = player()
        self.stage = stage(1, "Forest")
        self.zone = "Forest"
        self.stage_num = 1

        self.boss_timer = -1#the amount of time the player has to kill the boss
        #if this value is -1, the player is not fighting the boss

    #draw the player's stats at the top of the screen
    def draw_player(self):
        health = self.font.render("Health: " + str(self.player.get_health()), 1, (255,255,255))
        level = self.font.render("Level: " + str(self.player.get_level()), 1, (255,255,255))
        exp = self.font.render("Exp: " + str(self.player.get_exp()), 1, (255,255,255))
        gold = self.font.render("Gold: " + str(self.player.get_gold()), 1, (255,255,255))
        crit = self.font.render("Crit: " + str(self.player.get_crit_multiplier()), 1, (255,255,255))
        damage = self.font.render("Damage: " + str(self.player.get_damage_multiplier()), 1, (255,255,255))
        self.screen.blit(health, (0,0))
        self.screen.blit(level, (0,30))
        self.screen.blit(exp, (0,60))
        self.screen.blit(gold, (0,90))
        self.screen.blit(crit, (0,120))
        self.screen.blit(damage, (0,150))
    #draw the current stage
    def draw_stage(self):
        stage = self.font.render("Stage: " + str(self.stage_num), 1, (255,255,255))
        self.screen.blit(stage, (400,0))
    #draw the current zone as the background
    def draw_zone(self):
        self.screen.blit(regions_images[self.zone], (0,180))
    #draw the enemies in the current stage and their health
    def draw_enemies(self):
        self.screen.blit(enemies_images[self.stage.get_current_enemy().get_type()], (400,180))
        health = self.font.render("Health: " + str(self.stage.get_current_enemy().get_health()), 1, (255,255,255))
        self.screen.blit(health, (400,300))
    #draw the stats of the current stage
    def draw_stats(self):
        enemies = self.font.render("Enemies: " + str(self.stage.get_num_enemies()), 1, (255,255,255))
        self.screen.blit(enemies, (400,330))

    #draw the game screen
    def draw_screen(self):
        self.screen.fill((0,0,0))
        self.draw_player()
        self.draw_stage()
        self.draw_enemies()
        self.draw_stats()
        self.draw_zone()
        pygame.display.flip()

    #in the event that the player clears a stage, let them pick the next zone type from two options
    def pick_zone(self):
        zone1 = random.choice(list(regions_dict.keys()))
        zone2 = random.choice(list(regions_dict.keys()))
        while zone1 == zone2:
            zone2 = random.choice(list(regions_dict.keys()))
        zone1 = self.font.render(zone1, 1, (255,255,255))
        zone2 = self.font.render(zone2, 1, (255,255,255))
        self.screen.blit(zone1, (0,0))
        self.screen.blit(zone2, (0,30))
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                #if the mouse is clicked, find out where it was clicked and react accordingly 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    #if the player clicks on the first zone, set the zone to that zone
                    if mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 0 and mouse_pos[1] <= 30:
                        self.zone = zone1
                        return
                    #if the player clicks on the second zone, set the zone to that zone
                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 30 and mouse_pos[1] <= 60:
                        self.zone = zone2
                        return
    #after completing 10 stages, the player can reincarnate, 
    # resetting their stats except for one which they can select 
    def reincarnate(self):
        pygame.display.flip()
        #dipslay 3 buttons, one for each stat, all other screen elements should be cleared
        #the player can click on one of the buttons to reincarnate with that stat
        #blit the top highest button, which is the crit button, it should be a rectangle with the word crit in it
        self.screen.blit(pygame.image.load("crit_button.png"), (0,180))
        #blit the middle button, which is the damage button, it should be a rectangle with the word damage in it
        self.screen.blit(pygame.image.load("damage_button.png"), (0,230))
        #blit the bottom button, which is the health button, it should be a rectangle with the word health in it
        self.screen.blit(pygame.image.load("health_button.png"), (0,280))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #if the mouse is clicked check it's posiiton 
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    #if the player clicks on the crit button, reincarnate with crit
                    if mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 180 and mouse_pos[1] <= 230:
                        tempcrit = self.player.get_crit_multiplier()
                        self.player = player()
                        self.player.crit_multiplier = tempcrit
                        return
                    #if the player clicks on the damage button, reincarnate with damage
                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 230 and mouse_pos[1] <= 280:
                        tempdamage = self.player.get_damage_multiplier()
                        self.player = player()
                        self.player.damage_multiplier = tempdamage
                        return
                    #if the player clicks on the health button, reincarnate with health
                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 280 and mouse_pos[1] <= 330:
                        temphealth = self.player.get_health()
                        self.player = player()
                        self.player.health = temphealth
                        return
                    
                    
                    

    #handle the player's input
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            #if the mouse is clicked, find out where it was clicked and react accordingly 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                #if the player clicks on the enemy, deal damage to the enemy
                if mouse_pos[0] >= 400 and mouse_pos[0] <= 500 and mouse_pos[1] >= 180 and mouse_pos[1] <= 280:
                    self.player.deal_damage(self.stage.get_current_enemy(), 0) #TODO add crit
                    #if the damage kills the enemy, remove it from the stage and give the player exp and gold
                    if self.stage.get_current_enemy().is_dead():
                        self.stage.kill_current_enemy()
                        self.player.gain_exp(random.randomint(1,3)*self.stage.get_stage_num())
                        self.player.gain_gold(random.randomint(1,3)*self.stage.get_stage_num())
                    #if this results in the boss being the only enemy left, start the boss timer
                        if self.stage.get_num_enemies() == 1:
                            self.boss_timer = 3000 #equivalent to 3000/60 seconds so 50 seconds
                    #if this results in the stage being cleared, let the player pick the next zone
                        if self.stage.is_stage_complete():
                            self.pick_zone()
                            self.stage_num += 1
                    #if this results in the 10th stage being cleared, then do the reincarnation procedure
            
                #if the player clicks on the upgrade crit button, upgrade their crit
                elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 180 and mouse_pos[1] <= 230:
                    if self.player.get_gold() >= int(10*self.player.get_crit_multiplier()):
                        self.player.upgrade_crit()
                        self.player.spend_gold(int(10*self.player.get_crit_multiplier()))
                    else:
                        print("Not enough gold")

                #if the player clicks on the upgrade damage button, upgrade their damage
                elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 230 and mouse_pos[1] <= 280:
                    if self.player.get_gold() >= int(10*self.player.get_damage_multiplier()):
                        self.player.upgrade_damage()
                        self.player.spend_gold(int(10*self.player.get_damage_multiplier()))
                    else:
                        print("Not enough gold")

                #if the player clicks on the restore health button, restore their health
                elif mouse_pos[0] >= 0 and mouse_pos[0] <= 200 and mouse_pos[1] >= 280 and mouse_pos[1] <= 330:
                    if self.player.get_gold() >= 10:
                        self.player.restore_health()
                        self.player.spend_gold(10)
                    else:
                        print("Not enough gold")
                
    #run the game
    def run(self):
        while True:
            self.handle_input()
            self.draw_screen()
            self.clock.tick(60)
            #if the player is fighting the boss, decrement the timer
            if self.boss_timer > 0:
                self.boss_timer -= 60
            #if the timer runs out, reset the stage, with the same zone
            elif self.boss_timer == 0:
                self.stage = stage(self.stage_num, self.zone)
                self.boss_timer = -1
            
#run the game
game = game_runner()
game.run()

    




    
        
    

    
        







