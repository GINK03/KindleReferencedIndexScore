import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
import scala.collection.mutable.{ListBuffer}
object Main {
  def main(args: Array[String]){
    val n = readLine().toInt
    val s = (readLine() + readLine())
    val a = s.toList.zipWithIndex.map { case (x,i) => List(i,x.toChar.toString) }.filter { x => x(1) == "x"}
    val reps = a.combinations(n).flatMap {x=> x.permutations}.toList.map { x => 
      var sl:ListBuffer[Char] = s.toList.to[ListBuffer]
      x.map { x2 => 
        val (i, x ) = (x2(0).asInstanceOf[Int], x2(1))
        sl(i) = 'o'.toChar
      } 
      sl.mkString("")
    } 
    val ranks = reps.map { x=>
      val splited = x.split("x").toList.sortWith { (a, b) => a.length > b.length }
      if (splited == List())
        0
      else 
        splited.head.length
    }.sortWith( (a, b) => a > b )
    println(reps)
    println(ranks.max)
  }
}
