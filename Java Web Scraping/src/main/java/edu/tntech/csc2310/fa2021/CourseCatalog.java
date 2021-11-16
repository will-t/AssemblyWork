package edu.tntech.csc2310.fa2021;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.*;

public class CourseCatalog {

    public String getSubject () {
        return Subject;
    }

    public void setSubject (String subject){
        Subject = subject;
    }

    public String getCatalogYear () {
        return catalogYear;
    }

    public void setCatalogYear (String catalogYear){
        this.catalogYear = catalogYear;
    }

        private ArrayList<Course> db;
        String Subject = new String();
        String catalogYear = new String();
        private String Number;
    public Course getCourse (String Number){
        for(int i = 0; i < db.size(); i++){
            if(db.get(i).getNumber().equals(Number)){
                return db.get(i);
            }
        }
        return null;
    }
    public CourseCatalog(String Subject, String catalogYear) throws IOException {


            this.Subject = Subject;
            this.catalogYear = catalogYear;
        db = new ArrayList();
        Document doc = Jsoup.connect("https://ttuss1.tntech.edu/PROD/bwckctlg.p_display_courses?sel_crse_strt=1000&sel_crse_end=4999&sel_subj=&sel_levl=&sel_schd=&sel_coll=&sel_divs=&sel_dept=&sel_attr=&term_in="+catalogYear+"&one_subj="+Subject+"" ).get();
        Elements courseCat = doc.select(".nttitle");
        String courseCat2 = courseCat.get(0).text();
        for (int i =0; i < courseCat.size(); i++) {
            String courseCat123 = courseCat2.substring(courseCat2.lastIndexOf("-") - 5);
            //courseCat123 = courseCat123.replace(" -", "");
            //courseCat123 = courseCat123.substring(courseCat123.indexOf("-"));
            //courseCat123 = courseCat123.substring(courseCat123.indexOf("CSC")+ 8);
             courseCat123 = courseCat123.substring(0,courseCat123.indexOf("-"));
             courseCat123 = courseCat123.replace(" ", "");
            db.add(new Course(Subject, courseCat123 , catalogYear));


        }
//    public Course getCourse(String Number){
//    }





}


}
