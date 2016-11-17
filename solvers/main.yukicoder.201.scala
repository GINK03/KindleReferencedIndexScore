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
    var dmap:Map[BigDecimal,String] = Map()
    val s = (readLine() + " " + readLine()).split(" ").toList
    val (n1, p1, g1, n2, p2, g2) = (s(0), BigDecimal(s(1)), s(2), s(3), BigDecimal(s(4)), s(5))
    dmap ++= Map(p1 -> n1)
    dmap ++= Map(p2 -> n2)
    val max = List(p1, p2).max
    if ( p1 == p2 ) { 
      println(-1)
      return
    }
    println(dmap(max))
    
  }
}
