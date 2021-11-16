import java.util.Date;

public class DailyGrind{
public static final void main(String[] args){

boolean its_time_to_go_home = false;
boolean away_the_hours = true;

while (away_the_hours) {
  boolean away_the_hours = true;

  Date now = new Date();
  its_time_to_go_home = now.getHours() > 17
  && now.getMinutes() > 30;

  	if (its_time_to_go_home) {
            break;
try {
      Thread.sleep(60000);
 } catch (InterruptedException e) {
 	// ignore
 }
      }






}


}
