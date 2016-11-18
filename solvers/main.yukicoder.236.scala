import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks

object Main {
  val inf = Stream.continually(List(None, None, Some("Fizz")).toStream).flatten
  val inf2 = Stream.from(1)
  val inf3 = Stream.continually(1)
  val _lmax  = Long.MaxValue
  val _imax  = Int.MaxValue
  val b1   = new Breaks
  def main(args: Array[String]){
   val inputs = readLine().split(" ").map { x => x.toInt}
   val (a, b, x, y) = (inputs(0), inputs(1), inputs(2), inputs(3)) 
   val (need_x, need_y) = (x*b/a.toDouble, y*a/b.toDouble)
   if ( need_x < y ) {
     println(need_x+x)
   } else {
     println(need_y+y)
   }
  }
}
