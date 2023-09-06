from typing import List, Tuple
import pygame
from math import sqrt, sinh, exp

class Robot:
    def __init__(self, scale_meter2px:float, rz:float = 0.3, pos:List = [0,0], vel:List = [0,0], ctr:str = "csch") -> None:
        self.RobotSize = rz
        self.position = pos
        self.velocity = vel # linear and angular
        self.scale_meter2px = scale_meter2px
        rz_px = rz*scale_meter2px
        self.pyrect = pygame.Rect(0, 0, rz_px, rz_px)
        self.pyrect.centerx = pos[0]*scale_meter2px
        self.pyrect.centery = pos[1]*scale_meter2px
        self.Neighbors:List[Tuple[Robot, float]] = []
        self.ctrlType = ctr
        self.v = 0

    def update(self, ts:float) -> None:
        # ts in miliseconds
        dx, dy = 0, 0
        for neigh in self.Neighbors:
            ddx, ddy = 0, 0
            if self.ctrlType == "csch":
                ddx, ddy = self.consensus_csch(neigh)
            elif self.ctrlType == "exp":
                ddx, ddy = self.consensus_exp(neigh)
            dx -= ddx
            dy -= ddy

        self.velocity = [dx, dy]
        self.position[0] += self.velocity[0] * (ts / 1000.0)
        self.position[1] += self.velocity[1] * (ts / 1000.0)
        self.pyrect.centerx = self.position[0] * self.scale_meter2px
        self.pyrect.centery = self.position[1] * self.scale_meter2px

    def add_links(self, links) -> None:
        self.Neighbors = links
        # print(self.Neighbors)

    def consensus_gdesc(self, neigh) -> Tuple:
        alpha, delta, k = 1.0, 0.2, 0.25*neigh[1]
        beta = 0.5
        l = (self.position[0] - neigh[0].position[0], self.position[1] - neigh[0].position[1])
        norm_l = sqrt(l[0]**2 + l[1]**2)
        exp_ = exp(-(norm_l - delta)**2 / k)
        self.v = beta * self.v + alpha*(1 - 10.0*exp_ )
        dx = self.v*l[0]
        dy = self.v*l[1]
        return dx, dy
    
    def consensus_exp(self, neigh) -> Tuple:
        alpha, delta, k = 1.0, 0.2, 0.25*neigh[1]
        l = (self.position[0] - neigh[0].position[0], self.position[1] - neigh[0].position[1])
        norm_l = sqrt(l[0]**2 + l[1]**2)
        exp_ = exp(-(norm_l - delta)**2 / k)
        w = alpha*(1 - 10.0*exp_ )
        dx = w*l[0]
        dy = w*l[1]
        return dx, dy

    def consensus_csch(self, neigh) -> Tuple:
        alpha, delta, k = 1.0, 0.2, neigh[1]
        l = (self.position[0] - neigh[0].position[0], self.position[1] - neigh[0].position[1])
        norm_l = sqrt(l[0]**2 + l[1]**2)
        csch_ = self.csch((norm_l - delta) / k)
        w = alpha*(1 - (1/(k * norm_l))*csch_**2 )
        dx = w*l[0]
        dy = w*l[1]
        return dx, dy

    def csch(self, x:float) -> float:
        if x == 0:
            return float('inf')
        return 1 / sinh(x)



class Consensus:
    def __init__(self, positions:List[Tuple], scale_meter2px:float, ctr:str = "csch") -> None:
        self.scale_meter2px = scale_meter2px
        self.font = pygame.font.Font(None, 36)
        self.robots:List[Robot] = []
        for pos in positions:
            self.robots += [Robot(scale_meter2px, pos=pos, ctr=ctr)]
    
    def create_formation(self, links:List[List[Tuple[int, float]]]):
        for i, link in enumerate(links):
            robots_neigh = [(self.robots[j], k) for j, k in link]
            self.robots[i].add_links(robots_neigh)
    
    def update(self, ts:float) -> None:
        for robot in self.robots:
            robot.update(ts)

    def draw_formation(self, screen):
        for i, robot in enumerate(self.robots):
            pygame.draw.ellipse(screen, (255,255,255), robot.pyrect)
            start = (robot.pyrect.x + robot.RobotSize*self.scale_meter2px//2,
                    robot.pyrect.y + robot.RobotSize*self.scale_meter2px//2)
            
            text_surface = self.font.render(str(i), True, (140,140,140))
            # Get the text's bounding rectangle
            text_rect = text_surface.get_rect()
            # Center the text on the screen
            text_rect.center = (start[0], start[1])
            # Draw the text on the screen
            screen.blit(text_surface, text_rect)
            for neigh in robot.Neighbors:
                end = (neigh[0].pyrect.x + neigh[0].RobotSize*self.scale_meter2px//2, 
                        neigh[0].pyrect.y + neigh[0].RobotSize*self.scale_meter2px//2)
                pygame.draw.line(screen, (180,180,180), start, end, 3)
                
