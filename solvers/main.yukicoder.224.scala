import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks

object Main {
  val inf2 = Stream.from(1)
  val inf3 = Stream.continually(1)
  val _lmax  = Long.MaxValue
  val _imax  = Int.MaxValue
  val b1   = new Breaks
  def main(args: Array[String]){
    val n   = readLine().toInt
    val s1  = readLine().toList
    val s2  = readLine().toList
    println(s1.zip(s2).filter { x=> x._1 != x._2 }.length )
  }
}
