import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  val b1   = new Breaks
  def main(args: Array[String]){
    val ns = readLine().split(" ").map { x => x.toInt}
    val (p, c) = (ns(0), ns(1))
    println(pow(41,p) * pow(49,c)/pow(6, p+c).toDouble)
  }
}
