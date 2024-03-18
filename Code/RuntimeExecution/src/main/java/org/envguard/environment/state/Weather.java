package org.envguard.environment.state;

public class Weather {
    private String value;

    public Weather() {
        super();
        this.value = "";
    }

    public int enableChange(String value) {
        if (this.value.equals(value)) {
            return 0;
        } else {
            return 1;
        }
    }

    public void extActionChange(String value) {
        if (enableChange(value) == 1) {
            this.value = value;
        }
    }

    public String get() {
        return this.value;
    }
}