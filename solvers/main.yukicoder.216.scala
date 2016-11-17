import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  val inf2 = Stream.from(1)
  val inf3 = Stream.continually(1)
  val _lmax  = Long.MaxValue
  val _imax  = Int.MaxValue
  val b1   = new Breaks
  def main(args: Array[String]){
    val n = readLine().toInt
    val points = readLine().split(" ").map { x => x.toInt }.toList
    val whos   = readLine().split(" ").map { x => x.toInt }.toList
    var dmap:Map[Int,Int] = Map()
    points.zip(whos).map { (xs) =>
      val (point, who) = (xs._1, xs._2)
      if (dmap.get(who) == None) 
        dmap = dmap ++ Map(who -> point)
      else
        dmap(who) += point
    }
    val conved = dmap.map { xs => 
      val (k, v) = (xs._1, xs._2)
      List(k, v)
    }.toList.sortWith { (a,b) => a(1) > b(1)} 
    val first = conved(0)
    val kkuns = conved.filter { x =>  x(0) == 0 }
    val others= conved.filter { x =>  x(0) != 0 }
    if (kkuns.length == 0){
      println("NO")
      return
    }
    if (others.length == 0){
      println("YES")
      return
    }
    val gettable = kkuns(0)(1)
    val maxpoint = others(0)(1)
    if (gettable >= maxpoint) 
      println("YES")
    else
      println("NO")
  }
}
