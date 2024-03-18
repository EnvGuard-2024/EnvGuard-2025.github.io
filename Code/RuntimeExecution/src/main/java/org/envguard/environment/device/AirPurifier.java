package org.envguard.environment.device;

public class AirPurifier {
    private int on;

    public AirPurifier() {
        super();
        this.on = 0;
    }

    public int enableOn() {
        if (this.on == 1) {
            return 0;
        } else {
            return 1;
        }
    }

    public void actionOn() {
        if (enableOn() == 1) {
            this.on = 1;
        }
    }

    public int enableOff() {
        if (this.on == 0) {
            return 0;
        } else {
            return 1;
        }
    }

    public void actionOff() {
        if (enableOff() == 1) {
            this.on = 0;
        }
    }

    public int get() {
        return this.on;
    }
}