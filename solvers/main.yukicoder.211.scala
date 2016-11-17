import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  val b1   = new Breaks
  def main(args: Array[String]){
    val n = readLine().toInt
    val primes = "2,3,5,7,11,13".split(",").map { x => x.toInt }.toList
    val combines = "4,6,8,9,10,12".split(",").map { x => x.toInt }.toList
    var dmap:Map[Int,Int] = Map()
    primes.map { p => 
      combines.map { c => 
        if (dmap.get(p*c) == None) dmap = dmap ++ Map(p*c -> 0)
        dmap(p*c) += 1
      }
    }
    if (dmap.get(n) == None) {
      println("0.0")
      return
    }
    println(dmap(n)/dmap.values.sum.toDouble)
  }
}
