import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
import scala.collection.mutable.{ListBuffer}
import scala.math.{ BigDecimal }
object Main {
  def main(args: Array[String]){
    val n = readLine().toInt
    val votes = readLine().split(" ").map { x => x.toInt }
    val ave = votes.reduceLeft { (a, x) => a +x }/10.0
    val v = votes.filter { x => x <= ave }.map { x => 30 }.toList
    var money = 0
    if ( v != List() )  money = v.reduceLeft { (a, x) => a +x } 
      
    println(money)
  }
}
