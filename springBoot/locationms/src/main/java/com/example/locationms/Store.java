package com.example.locationms;

public class Store {

    private String location;
    private float longitude;
    private float latitude;

    public Store(String location_, float longitude_, float latitude_){
        this.location = location_;
        this.longitude = longitude_;
        this.latitude = latitude_;
    }

//    public static void store(String[] args){
//        // longitude 103.852119f is float 103.85211 is double
//        Store S1 = new Store("SMU Store", 103.852119f, 1.296568f);
//        Store S2 = new Store("Tampines Store", 103.956788f, 1.349591f);
//    }

    public float getLong(){
        return longitude;
    }
    public double getLat(){
        return latitude;
    }

    public String getLocation(){ return location; }
}