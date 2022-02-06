<template>
  <div class="home">
    <el-row display="margin-bottom: 1rem">
      <el-button @click="restartInit()" style="float:left ; background: bisque; padding: 10px 12px; border-radius: 6px; font-size: 6px; cursor: pointer ">重新开始</el-button>
      <el-button @click="regret()" style="float:10px ; background: bisque; padding: 10px 12px; border-radius: 6px; font-size: 6px; cursor: pointer ">悔棋</el-button>
      <el-button @click="undo()" style="float:right ; background: bisque; padding: 10px 12px; border-radius: 6px; font-size: 6px; cursor: pointer ">撤销悔棋</el-button>
    </el-row>
    <el-row display="margin-top:10px">
      <el-input v-model="size" placeholder="请输入棋盘大小" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-button @click="makeSize()" style="float:left; margin: 2px;">确认</el-button>
    </el-row>
    <el-row display="margin-top:10px">
      <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
      <el-button @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
    </el-row>
    <el-row display="margin-bottom:20px">
      <template>
        <el-button @click="drawpieceBoard()" style="margin: 2px;">画图</el-button>
      </template>
    </el-row>
  </div>
</template>

<script>
  export default {
    name: 'home',
    data() {
      return {
        input: '',
        bookList: [],
        size: 15,
        pieceMapArr: [], //记录棋盘落子情况
        pieceColor: ["black", "white"], //棋子颜色
        step: 0, //记录当前步数
        checkMode: [ //输赢检查方向模式
          [1, 0], //水平
          [0, 1], //竖直
          [1, 1], //左斜线
          [1, -1], //右斜线
        ],
        flag: false,
        victory: '',
        history: [], //历史记录位置
        historyVal: [], //历史记录不被删除数组
        stepHistory: 0,
        domPiece: [], //
        log:'',
        toggle: true //true为canvas,false为dom
       
      }
    },

    mounted() {
      const myCanvas = document.getElementById("myCanvas");
      if (!myCanvas.getContext) {
        alert("当前浏览器不支持Canvas.");
        this.toggle = false;
        this.drawpieceBoardDom();
      } else {
        console.log("当前浏览器支持Canvas", this.toggle)

        this.drawpieceBoard();
        const canvas = this.$refs.canvas;
        // 添加点击监听事件
        canvas.addEventListener("click", e => {
          if (this.flag) {
            alert("游戏结束,请重新开始~");
            return;
          }
        });
      }
    },

    methods: {
      restartInit() {
        if (!this.toggle) {
          // console.log("-----dom-------")
          var elem = document.querySelector('#box01');
          // console.log("elem",elem)
          if (elem != null) {
            elem.parentNode.removeChild(elem);
            let elem02 = document.querySelector('#box02');
            elem02.parentNode.removeChild(elem02);
          }
          this.drawpieceBoardDom();
          this.flag = false;
          this.step = 0;
          this.stepHistory = 0;
          this.historyVal = [];
          this.history = [];
        } else {
          //重画
          this.repaint();
          // 绘制棋盘
          this.drawpieceBoard();
          this.flag = false;
          this.step = 0;
          this.stepHistory = 0;
          this.historyVal = [];
          this.history = [];
        }
      },

      drawpieceBoard() {
        const myCanvas = document.getElementById("myCanvas");
        if (!myCanvas.getContext)
          alert("不支持")
        //canvas 绘制
        let canvas = this.$refs.canvas;
        console.log('今天画图了吗', this.log)
        // 调用canvas元素的getContext 方法访问获取2d渲染的上下文
        let context = canvas.getContext("2d");
        context.strokeStyle = '#666'
        for (let i = 0; i <= 15; i++) {
          //落在方格(canvas 的宽高是450)
          context.moveTo(15 + i * 30, 15)
          context.lineTo(15 + i * 30, 465)
          context.stroke()
          context.moveTo(15, 15 + i * 30)
          context.lineTo(465, 15 + i * 30)
          context.stroke()
        }
      },

      //绘制棋子
      drawPiece(x, y, color) {
        let canvas = this.$refs.canvas
        let context = canvas.getContext("2d");
        context.beginPath(); //开始一条路径或重置当前的路径
        context.arc(x, y, 13, 0, Math.PI * 2, false);
        context.closePath();
        context.fillStyle = color;
        context.fill();
      },

      makeSize() {
        this.$http.get('http://127.0.0.1:8000/api/makeSize?size=' + this.size)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num == 0) {
              this.size = res['size']
            } else {
              this.$message.error('设置棋盘大小失败，请重试')
              console.log(res['msg'])
            }
          }
          )
      },

      regret() {
        alert("regret")
      },

      undo() {
        alert("undo")
      },

      addBook() {
        this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            if (res.error_num === 0) {
              this.showBooks()
            } else {
              this.$message.error('新增书籍失败，请重试')
              console.log(res['msg'])
            }
          })
      },
      showBooks() {
        this.$http.get('http://127.0.0.1:8000/api/show_books')
          .then((response) => {
            var res = JSON.parse(response.bodyText)
            console.log(res)
            if (res.error_num === 0) {
              this.bookList = res['list']
            } else {
              this.$message.error('查询书籍失败')
              console.log(res['msg'])
            }
          })
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }

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

  .restart, .regret, .undo {
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
