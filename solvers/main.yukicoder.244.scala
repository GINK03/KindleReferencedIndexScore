import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike

object Main {
  def main(args: Array[String]){
    var ar2x = Array(Array())
    readLine().split(" ").zipWithIndex.map { case (x,i) => 
      println(x,i)
    }
  }
}
