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
    val ins  = readLine().replaceAll("o", "1").replaceAll("x", "0")
    val n    = readLine().toInt
    val outs = readLine().replaceAll("o", "1").replaceAll("x", "0")
    val sints = ins.toList.sortBy(_.toInt)
    val souts = outs.toList.sortBy(_.toInt)
    if (sints != souts) {
      println("SUCCESS")
      return
    }
    if (n >= 2 ) {
      println("FAILURE")
      return 
    }
    if ( n == 0) {
      if ( ins != outs ) println("SUCCESS")
      else println("FAILURE")
      return
    }
    val m:Map[String, List[String]] = Map( "111" -> List("111"), "000" -> List("000"), "100" -> List("100", "010"), "010" -> List("100", "001"), "110" -> List("110", "101"), "011" -> List("101", "011"), "001" -> List("001", "010"), "101" -> List("011", "110") )
    if ( n == 1 ) {
      val swappable = m(ins).contains(outs)
      if (swappable) println("FAILURE")
      else println("SUCCESS")
    }
  }
}
