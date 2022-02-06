<template>
  <div class="home">
    <el-row display="margin-bottom: 1rem">
      <el-button @click="restartInit()" style="float:left; background: bisque; margin: 12px; cursor: pointer">重新开始</el-button>
      <el-button @click="regret()" style=" background: bisque; margin: 12px; cursor: pointer">悔棋</el-button>
    </el-row>
    <el-row class="chess" display="margin-top:10px">
      <el-input v-model="size" placeholder="请输入棋盘大小" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-button @click="makeSize()" style="margin: 2px;">确认</el-button>
    </el-row>
    <canvas id="myCanvas" ref="canvas" width="480" height="480">当前浏览器不支持Canvas</canvas>
  </div>
</template>

<script>
  export default {
    name: 'chess',
    data() {
      return {
        size: '11',
        mid: 0,
        pieceMapArr: [], //记录棋盘落子情况
        pieceColor: ["black", "red"],//棋子颜色
        step: 0, //记录当前步数
        x1: -1,
        y1: -1,
        x2: -1,
        y2: -1,
        flag: false,
        endness: '',
        toggle: true //true为canvas,false为dom
      }
    },
    mounted() {
      const myCanvas = document.getElementById("myCanvas");
      if (!myCanvas.getContext) {
        alert("当前浏览器不支持Canvas.");
        this.toggle = false;
        return;
      } else {
        console.log("当前浏览器支持Canvas", this.toggle)
        this.initPieceArr();
        this.repaint();
        this.drawpieceBoard(this.pieceMapArr);
        const canvas = this.$refs.canvas;
        // 添加点击监听事件
        canvas.addEventListener("click", e => {
          if (this.flag) {
            alert("游戏结束,请重新开始~");
            return;
          }
          //判断点击范围是否越出棋盘
          if (e.offsetX < 25 || e.offsetX > 450 || e.offsetY < 25 || e.offsetY > 450) {
            return;
          }
          let dx = Math.floor((e.offsetX + 15) / 30) * 30;
          let dy = Math.floor((e.offsetY + 15) / 30) * 30;
          //传送棋子位置
          //this.sendPos();
          //画棋子
          if (this.pieceMapArr[dx / 30][dy / 30] != 0) {   //如果这个位置有棋子

            let x = dx / 30;
            let y = dy / 30;

            if (this.x1 == -1) {  //点击的第一个棋子
              this.x1 = x;
              this.y1 = y;
              this.drawPiece(x, y, this.pieceColor[1]); //点击棋子变红
              console.log("点击第一个位置：", this.x1, this.y1)
            } else {   //点击的第二个棋子
              this.x2 = x;
              this.y2 = y;
              console.log("点击第二个位置：", this.x2, this.y2)

              let move = this.judgeMove(this.x1, this.y1, this.x2, this.y2);
              console.log("move:", move)
              if (move != -1) {    //如果是相邻的棋子
                //this.drawPiece(dx, dy, this.pieceColor[1]); //点击棋子变红
                console.log("相邻", move)
                this.drawPiece(this.x2, this.y2, 'bisque');
                this.drawPiece(this.x1, this.y1, 'bisque');
                this.pieceMapArr[this.x1][this.y1] = 0;  //在棋盘上消除两个棋子
                this.pieceMapArr[this.x2][this.y2] = 0;

                switch (move) {
                  case 1:
                    this.pieceMapArr[this.x1][this.y1 + 2] = 1;
                    this.drawPiece(this.x1, (this.y1 + 2), this.pieceColor[0]);
                    break;
                  case 2:
                    this.pieceMapArr[this.x1][this.y1 - 2] = 1;
                    this.drawPiece(this.x1, this.y1 - 2, this.pieceColor[0]);
                    break;
                  case 3:
                    this.pieceMapArr[this.x1 - 2][this.y1] = 1;
                    this.drawPiece(this.x1 - 2, this.y1, this.pieceColor[0]);
                    break;
                  case 4:
                    this.pieceMapArr[this.x1 + 2][this.y1] = 1;
                    this.drawPiece(this.x1 + 2, this.y1, this.pieceColor[0]);
                    break;
                  default:
                    return;
                }
                //this.sendPos();
              } else {   //如果是非相邻的
                if (this.pieceMapArr[this.x1][this.y1] != 0)
                  this.drawPiece(this.x1, this.y1, this.pieceColor[0]);  //将第一个棋子涂为黑色
              }
              this.x1 = -1;
              this.y1 = -1;
            }
            this.step++;
          } else {
            alert("不可移动空位！");
          }
        });
      }
    },
    methods: {
      //确定棋盘大小
      makeSize() {
        this.$http.get('http://127.0.0.1:8000/api/make_size', { params: { size: this.size } })
          .then((response) => {   //response是页面获取的结果
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
            } else {
              this.$message.error('设置棋盘大小失败，请重试')
              console.log(res['msg'])
            }
          })
        this.repaint();
        this.initPieceArr();
        this.drawpieceBoard(this.pieceMapArr);
        this.flag = false;
        this.step = 0;
      },
      //判断是否结束
      checkEnd() {
        this.$http.get('http://127.0.0.1:8000/api/checkend')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.end == true) {
              this.endness = "本局已无法继续移动棋子";
              this.flag = true
            }
          }
          )
      },
      //传送棋子位置
      sendPos() {
        this.$http.post('http://127.0.0.1:8000/api/sendpos', { x1: this.x1, y1: this.y1, x2: this.x2, y2: this.y2 })
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 1) {
              this.$message.error('传送棋子位置失败')
              console.log(res['msg'])
            }
          })
      },
      //判断棋子是否可以移动
      judgeMove(x1, y1, x2, y2) {
        if (x2 == x1 && y2 == y1 + 1 && this.pieceMapArr[x1][y1 + 2] == 0) {
          return 1;
        } else if (x2 == x1 && y2 == y1 - 1 && this.pieceMapArr[x1][y1 - 2] == 0) {
          return 2;
        } else if (x2 == x1 - 1 && y2 == y1 && this.pieceMapArr[x1 - 2][y1] == 0) {
          return 3;
        } else if (x2 == x1 + 1 && y2 == y1 && this.pieceMapArr[x1 + 2][y1] == 0) {
          return 4;
        } else {
          return -1;
        }
      },

      toggleF() {
        this.toggle = !this.toggle
        this.restartInit()
      },

      //初始化棋盘数组
      initPieceArr() {
        this.pieceMapArr = [];
        for (let i = 0; i <= this.size; i++) {
          this.pieceMapArr[i] = [];
          for (let j = 0; j <= this.size; j++) {
            this.pieceMapArr[i][j] = 1;
          }
        }
        this.mid = Math.floor(this.size / 2 + 1);
        console.log("this.mid: ", this.mid)
        this.pieceMapArr[this.mid][this.mid] = 0;
      },
      //重新开始
      restartInit() {
        this.$http.get('http://127.0.0.1:8000/api/restart')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 1) {
              this.$message.error('重启失败，请重试')
            } else {
              if (this.toggle) {
                //重画
                this.repaint();
                this.initPieceArr();
                this.drawpieceBoard(this.pieceMapArr);
                this.flag = false;
                this.step = 0;
              }
            }
          })
      },

      //获取棋盘数组
      getPieceArray() {
        this.$http.get('http://127.0.0.1:8000/api/getpiecearray')
          .then((response) => {
            this.pieceMapArr = JSON.parse(response.bodyText)   //这里的response是二维数组类型的数据
          })
      },

      // 绘制棋盘
      drawpieceBoard(arr) {
        //初始化棋盘数组
        //this.pieceArr();
        //canvas 绘制
        let canvas = this.$refs.canvas
        // 调用canvas元素的getContext 方法访问获取2d渲染的上下文
        let context = canvas.getContext("2d");
        context.strokeStyle = '#666'

        for (let i = 0; i <= this.size; i++) {
          //落在方格(canvas 的宽高是450)
          context.moveTo(15 + i * 30, 15)
          context.lineTo(15 + i * 30, 15 * (this.size * 2 + 1))
          context.stroke()
          context.moveTo(15, 15 + i * 30)
          context.lineTo(15 * (this.size * 2 + 1), 15 + i * 30)
          context.stroke()
        }

        for (let i = 1; i <= this.size; i++) {
          for (let j = 1; j <= this.size; j++) {
            if (arr[i][j] != 0) {  //非0的数组位置棋子全都画成黑色
              this.drawPiece(i, j, this.pieceColor[0]);
            }
          }
        }
      },

      //绘制棋子
      drawPiece(x, y, color) {
        let dx = x * 30;
        let dy = y * 30
        let canvas = this.$refs.canvas
        let context = canvas.getContext("2d");
        context.beginPath(); //开始一条路径或重置当前的路径
        context.arc(dx, dy, 13, 0, Math.PI * 2, false);
        context.closePath();
        context.fillStyle = color;
        context.fill();
      },

      //重画
      repaint() {
        let canvas = this.$refs.canvas;
        let context = canvas.getContext("2d");
        canvas.width = this.size * 30 + 30;
        canvas.height = this.size * 30 + 30;
        //context.clearRect(0, 0, canvas.width, this.size * 30 + 30t);
        context.fillStyle = "bisque";
        //console.log("长宽：", canvas.width, canvas.height)
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.beginPath();
        context.closePath();
      },

      //悔棋:先获取历史记录，history是列表
      regret() {
        this.$http.get('http://127.0.0.1:8000/api/gethistory')
          .then((response) => {
            var history = JSON.parse(response.bodyText)
            if (this.toggle) {
              //重画
              this.repaint();
              // 绘制棋盘
              this.drawpieceBoard();
              //绘制棋子
              history.forEach(e => {
                this.drawPiece(e.dx, e.dy, e.color)
                this.pieceMapArr[e.dx / 30 - 1][e.dy / 30 - 1] = e.color;
              });
              this.step--;
              if (history.length == 0 || this.flag) {
                alert("已经不能悔棋了~")
              }
            }
          })
      },
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  body {
    margin: 0;
    padding: 0;
  }

  #app {
    padding-left: 30%;
    width: 500px;
  }

  .h2Title {
    text-align: center;
  }

  #app h3 {
    color: red;
  }

  .Fbuttons {
    margin-bottom: 1rem;
  }

  .main {
    background-color: bisque;
    width: 30rem;
  }

  .restart, .regret, .undo, .makesize {
    background: bisque;
    padding: 6px 10px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
  }

  #chess {
    position: relative;
    width: 440px;
    height: 450px;
    padding-left: 30px;
    padding-top: 30px;
    background-color: bisque;
  }

    #chess .squre {
      width: 28px;
      height: 28px;
      border: 1px solid #666;
      float: left;
    }

  #box01 .squre:hover {
    background-color: pink;
  }

  #box01 {
    position: absolute;
    margin: 0 auto;
    width: 450px;
    height: 450px;
    top: 15px;
    left: 15px;
  }

    #box01 .qz {
      /* width: 28px;
        height: 28px; */
      width: 30px;
      height: 30px;
      border: 0px solid #C7C7C7;
      float: left;
      border-radius: 50%;
      /* margin: 1px; */
    }

      #box01 .qz:hover {
        background-color: pink;
      }

  .toggle {
    float: right;
  }

  .size {
    float: center;
  }
</style>
