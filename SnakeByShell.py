import os,random
sw=[[5,7]]                                             #食物坐标对象
lc=[[5,i] for i in range(5)]                           #贪吃蛇坐标集对象
s=''                                                   #存储执行指令的对象
grass = [[x,y] for x in range(20) for y in range(20)]  #将地图坐标化，以坐标点组合的形式表示地图
field_sw = [var for var in grass if var not in lc]     #以差集的方式得到食物随机出现的范围（滤除贪吃蛇的坐标集）

if sw[0] in lc:                            #if语句检测食物是否在贪吃蛇内部
  del sw[0]                                #删除原有坐标
  sw.append(random.choice(field_sw))       #在贪吃蛇身体之外随机生成一个食物出现坐标
  print("Have Changed!")                   #测试用 

for x in range(500):                       #指令可以输入500次（贪吃蛇“寿命”500步）
  w=len(lc)-1                              #取贪吃蛇头部坐标索引
  li = [(['○'] * 20) for i in range(20)]  #创建20X20的地图背景
  a=input('请输入wasd控制:')               #获取输入的指令字符串
#  if a=='':
#     a=s
  if a=='w':                               #选择分支判断输入的指令执行“上下左右”对应操作
      lc.append([lc[w][0]-1,lc[w][1]])
      del lc[0]
      s='w'
  elif a=='s':
      lc.append([lc[w][0]+1,lc[w][1]])
      del lc[0]
      s='s'
  elif a=='a':
     lc.append([lc[w][0],lc[w][1]-1])
     del lc[0]
     s='a'
  elif a=='d':
     lc.append([lc[w][0],lc[w][1]+1])
     del lc[0]
     s='d'
  else:
    print("输入指令错误！")
    os.exit()
  if lc[w] in sw:                                           #判断贪吃蛇是否吃到食物
        lc.insert(0,[lc[0][0],lc[0][1]-1])                  #贪吃蛇身体长度+1

        field_sw = [var for var in grass if var not in lc]  #以差集滤除贪吃蛇的坐标集
        del sw[0]
        sw.append(random.choice(field_sw))                  #在不包含贪吃蛇的坐标集中随机生成食物坐标
        
  for i in lc:li[i[0]][i[1]]='●'                           #在地图背景中绘制贪吃蛇的身体
  for w in sw:li[w[0]][w[1]]='◆'                           #在地图背景中绘制食物
  os.system('clear')                                        #清除“痕迹”
  for i in li:print(''.join(i))                             #打印“渲染”

