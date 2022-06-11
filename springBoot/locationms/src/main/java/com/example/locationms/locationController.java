package com.example.locationms;

import org.springframework.web.bind.annotation.*;

@RestController
public class locationController {
    Store S1 = new Store("SMU Store", 103.852119f, 1.296568f);
    Store S2 = new Store("Tampines Store", 103.956788f, 1.349591f);
    Store ourStores[] = {S1, S2};

    public static double distance(double lat1, double lat2, double lon1, double lon2) {

        final int R = 6371; // Radius of the earth
        double latDistance = Math.toRadians(lat2 - lat1);
        double lonDistance = Math.toRadians(lon2 - lon1);
        double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                + Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2))
                * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        double distance = R * c;

        distance = Math.pow(distance, 2);

        return Math.sqrt(distance);
    }

    @RequestMapping(path = "/location", method = RequestMethod.POST)
    public LocationResponse location(@RequestBody Location location) {
        for (int i = 0; i < 2; i++) {
            System.out.println("Location: " + ourStores[i].getLocation());
            System.out.println("Long: " + location.getLong());
            System.out.println("Lat: " + location.getLat());
            System.out.println("Store Long: " + ourStores[i].getLong());
            System.out.println("Store Lat: " + ourStores[i].getLat());
            double distance = distance(location.getLat(), ourStores[i].getLat(), location.getLong(), ourStores[i].getLong());
            System.out.println("Distance: " + distance);
            if (distance < 5) {
              LocationResponse LocationResponse = new LocationResponse(200, ourStores[i].getLocation(), ourStores[i].getLat(), location.getLong(), distance);
              return LocationResponse;
            }
        }
        // not in any store
        LocationResponse LocationResponse = new LocationResponse(204, null, null, null, null);
        return LocationResponse;
    }
}