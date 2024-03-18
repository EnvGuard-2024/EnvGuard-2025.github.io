package org.envguard.environment.state;

public class Temperature {
    private int value;

    public Temperature() {
        super();
        this.value = 0;
    }

    public int enableDecrease() {
        if (this.value == -1) {
            return 0;
        } else {
            return 1;
        }
    }

    public int enableIncrease() {
        if (this.value == 1) {
            return 0;
        } else {
            return 1;
        }
    }

    public void extActionDecrease() {
        if (enableDecrease() == 1) {
            this.value = this.value - 1;
        }
    }

    public void extActionIncrease() {
        if (enableIncrease() == 1) {
            this.value = this.value + 1;
        }
    }

    public int get() {
        return this.value;
    }
}