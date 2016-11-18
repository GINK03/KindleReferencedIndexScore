import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  val b1   = new Breaks
  def main(args: Array[String]){
    val i = readLine().split(" ").map{ x => x.toInt }
    val (a, b) = (i(0), i(1))
    (a to b).map { x => 
      if (x.toString.contains("3") || x%3 == 0) println(x)
    }
  }
}
