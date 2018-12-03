#include <stdio.h>
#include <helpers.h>

long map(long x, long in_min, long in_max, long out_min, long out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

double map(double x, double in_min, double in_max, double out_min, double out_max) {
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void print_botball_logo() {
	printf("    ____  ____  __________  ___    __    __  \n");
	printf("   / __ )/ __ \\/_  __/ __ )/   |  / /   / / \n");
	printf("  / __  / / / / / / / __  / /| | / /   / /   \n");
	printf(" / /_/ / /_/ / / / / /_/ / ___ |/ /___/ /___ \n");
	printf("/_____/\\____/ /_/ /_____/_/  |_/_____/_____/\n");
	printf("============================================\n\n");
}