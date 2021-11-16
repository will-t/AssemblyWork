package edu.tntech.csc2310.fa2021;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;

public class Course {
        private String Subject;
        private String Number;
        private String Term;
        private String Description;
        private int Credits;
        private String [] Prerequisites;
    private String Title;
    public String getTerm() {
        return Term;
    }
        public String getSubject () throws Exception {
            return Subject;
        }
        public String getNumber () {
            return Number;
        }
        public String getTitle () {
            return Title;
        }
        public String getDescription() {
            return Description;
        }
        public int getCredits (){
            return Credits;
        }
        public String [] getPrerequisites() {
        return Prerequisites;

        }

//    public Course(String Subject, String Number, String Term){
//
//
//
//    }


//cc.substring(0, 3)
//cc.substring(4, 8)
//cc.substring(11);


    public Course(String Subject, String Number, String Term) throws IOException {
        this.Subject = Subject;
        this.Number = Number;
        this.Term =Term;

            Document doc = Jsoup.connect("https://ttuss1.tntech.edu/PROD/bwckctlg.p_disp_course_detail?cat_term_in=" + Term +"&subj_code_in=" + Subject + "&crse_numb_in="+Number).get();

            Elements courseCat = doc.select(".nttitle");
            for (int i = 0; i < courseCat.size(); i++) {
                String courses = courseCat.get(i).text();
                //System.out.println(courses);

                Title = courses.substring(courses.indexOf("- ")+ 2);
                for (int j = 0; j < courseCat.size(); j++) {
                    String cc = courseCat.get(i).text();





                }

            }
                Elements courseDef = doc.select(".ntdefault");
                String courseDefault = courseDef.get(0).text();
                // =courseDefault.substring("Prerequisite:"));
                Description = courseDefault.substring(0, courseDefault.indexOf("Levels"));
                Credits = Integer.parseInt(courseDefault.substring(courseDefault.indexOf("Credit hours")-6, courseDefault.indexOf("Credit hours")- 5));
             if(courseDefault.charAt(courseDefault.length()-1) == ')'){
                String Prerequisites123 = courseDefault.substring(courseDefault.indexOf("General Requirements:")+22);
                 Prerequisites123 = Prerequisites123.replace("( Course or Test: ", "");
                 Prerequisites123 = Prerequisites123.replace("Minimum Grade of D", "");
                 Prerequisites123 = Prerequisites123.replace("Minimum Grade of C", "");
                 Prerequisites123 = Prerequisites123.replace("May not be taken concurrently. ", "");
                 Prerequisites123 = Prerequisites123.replace("and ( Course or Test: ", "");
                 Prerequisites123 = Prerequisites123.replace("May be taken concurrently. )", "");
                 Prerequisites123 = Prerequisites123.replace(" and Course ", "");
                 Prerequisites123 = Prerequisites123.replace("Test: ", "");
                 Prerequisites123 = Prerequisites123.replace("  )", "");
                 Prerequisites123 = Prerequisites123.replace("(", "");
                 Prerequisites123 = Prerequisites123.replace(" )", "");
                 Prerequisites123 = Prerequisites123.replace("  ", "");
                 Prerequisites123 = Prerequisites123.replace("or", "or ");
                // Prerequisites123 = courseDefault.replace("May be taken concurrently. )", "");
                String [] requirArray = Prerequisites123.split(" or ");
                this.Prerequisites = requirArray;







             }






        }


        }

