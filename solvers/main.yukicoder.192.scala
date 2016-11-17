import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
import scala.collection.mutable.{ListBuffer}
import scala.math.{ BigDecimal }
object Main {
  def primesUnder(n: Int): List[Int] = {
    require(n >= 2)
    val primes = ListBuffer(2)
    for (i <- 3 to n) {
      if (prime(i, primes.iterator)) {
        primes += i
      }
    }
    primes.toList
  }
  def prime(num: Int, factors: Iterator[Int]): Boolean = 
    factors.takeWhile(_ <= math.sqrt(num).toInt) forall(num % _ != 0)

  def main(args: Array[String]){
    val n = readLine().toInt
    val ps = primesUnder(n+100)
    val evl = (n-100 to n+100).toList
    val rs = evl.filter { x =>
      var res = false
      ps.map { x2 =>
        if ( x%x2 == 0 && x != x2) res = true
      }
      res
    }
    println(rs.head)
    //(n-100 to n+100).map { 
  }
}
