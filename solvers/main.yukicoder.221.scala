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
    val k = 1000000/10000
    val mafia = readLine().toDouble * k
    val normal = 1000000 - mafia
    val P = 0.990

    val detected_mafia = mafia*P
    val detected_normal= normal*(1.0 - P)
    println( detected_normal/(detected_mafia+detected_normal)*100)
  }
}
