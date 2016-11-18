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
   var (head, min) = (pow(10,9), 1)
   //println("? " + min.toString)
   b1.breakable {
     inf2.take(100).toList.map { x => 
       val middle:Int = ((head+min)/2).toInt
       println("? " + middle.toString)
       val in = readLine().toInt
       if (in == 1 ) {
         min = middle
       } else {
         head = middle
       }
       if ( head - min <=  1) {
         println("? " + min.toString)
         if (readLine().toInt == 1) {
           println("! " + min.toString)
         } else {
           println("! " + head.toInt.toString)
         }
         b1.break
       }
     }
   }

  }
}
