import scala.io.StdIn.readLine
import scala.collection.immutable.StringLike
import scala.collection.immutable.Stream
import Math.{sqrt, pow}
import scala.util.control.Breaks
import scala.collection.mutable.{Map,SynchronizedMap, HashMap}
object Main {
  def main(args: Array[String]){
    val ns = """(o{1,})""".r.findAllIn( (0 to 1).map { x => readLine() }.mkString("") ). matchData.toList.map { m => m.toString}.sortWith( (a,b) => a.length > b.length)
    println(if (ns != List()) ns.head.length else  0 )
  }
}
