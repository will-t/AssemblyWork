package edu.tntech.csc2310.fa2021;

import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;

public class CourseCatalogTest {

    private CourseCatalog catalog;

    @Before
    public void setUp() throws Exception {
        catalog = new CourseCatalog("CSC", "202180");
    }

    @Test
    public void getCourse() {
        try {
            Course c = catalog.getCourse("2770");
            assertEquals("Course test", "Intro to Systems & Networking", c.getTitle());
            assertEquals("Course test credits", 3, c.getCredits());
            Course c1 = catalog.getCourse("2001");
            assertNull(c1);
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    @Test
    public void getCatalogYear() {
        assertEquals("Catalog Year", "202180", catalog.getCatalogYear());
    }

    @Test
    public void getSubject() {
        assertEquals("Subject", "CSC", catalog.getSubject());
    }
}