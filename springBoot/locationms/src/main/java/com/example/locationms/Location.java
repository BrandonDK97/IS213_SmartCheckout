package com.example.locationms;

public class Location {
    static double d_longitude;
    static double d_latitude;

    Location(double longitude,double latitude) {
        d_longitude = longitude;
        d_latitude = latitude;
    }
    public static double getLong(){
        return d_longitude;
    }
    public static double getLat(){
        return d_latitude;
    }

}
