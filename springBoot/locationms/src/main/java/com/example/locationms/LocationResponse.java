package com.example.locationms;

import org.springframework.beans.factory.annotation.Value;

public class LocationResponse {
    private int code;

    private String location;
    private double latitude;
    private double longitude;
    private double distance;

    LocationResponse(int code_, String location_, double latitude_, double longitude_, double distance_) {
        this.code = code_;
        this.location = location_;
        this.latitude = latitude_;
        this.longitude = longitude_;
        this.distance = distance_;
    }

    public LocationResponse(int code_, String location_, Double aDouble, Object o, Object o1) {
        this.code = code_;
    }

    public int getCode() {return code; }
    public String getLocation(){
        return location;
    }
    public double getLat(){return latitude;}
    public double getLong(){return longitude;}
    public double getDistance(){return distance;}
}