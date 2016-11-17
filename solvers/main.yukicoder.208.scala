import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  def main(args: Array[String]){
    val ns = (0 to 1).map { x => 
      readLine().split(" ").map { _.toInt}
    }.flatMap { x => x }
    val (x, y, x2, y2) = (ns(0), ns(1), ns(2), ns(3))
    val max = List(x, y).max
    if ( x != y ) {
      println(max)
      return 
    }
    if ( x == y && x2 < x && x2 == y2) 
      println(max+1)
    else
      println(max)
  }
}
