#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @Author: José Sánchez-Gallego (gallegoj@uw.edu)
# @Date: 2025-06-18
# @Filename: tools.py
# @License: BSD 3-clause (http://www.opensource.org/licenses/BSD-3-Clause)

from __future__ import annotations

import enum

from typing import TypedDict


__all__ = ["ScopeStatusMaskbit", "ScopeStatusDict", "parse_scope_status"]


class ScopeStatusMaskbit(enum.IntFlag):
    """Mask bits for the scope status."""

    INITIALIZED = 1
    TRACKING = 2
    SLEWING = 4
    PARKING = 8
    PARKED = 16
    LOOKING_EAST = 32
    BLINKY_MODE = 64
    COMMUNICATION_FAULT = 128
    LIMIT_SWITCH_PRIMARY_PLUS = 256
    LIMIT_SWITCH_PRIMARY_MINUS = 512
    LIMIT_SWITCH_SECONDARY_PLUS = 1024
    LIMIT_SWITCH_SECONDARY_MINUS = 2048
    HOMING_SWITCH_PRIMARY_AXIS = 4096
    HOMING_SWITCH_SECONDARY_AXIS = 8192
    ROTATOR_POSITION_COMMANDED = 16384
    TRACKING_OFFSET_RATE = 32768
    TRACKING_SATELLITE = 65536
    TRACKING_UNSETTLED_AFTER_SLEW = 131072


class ScopeStatusDict(TypedDict):
    """TypedDict for the parsed scope status."""

    bool_params: int
    bool_params_labels: list[str]
    right_ascension: float
    declination: float
    altitude: float
    azimuth: float
    secondary_axis_angle: float
    primary_axis_angle: float
    scope_sidereal_time: float
    scope_julian_day: float
    scope_time: float
    air_mass: float


def parse_scope_status(status: str) -> ScopeStatusDict:
    """Parses the ASCII ``ReadScopeStatus`` status string into a dictionary.

    From the documentation:

    As of version 0.92e, here is the standard return string description.

    The type (int, double, or string) is a literal string, your software must
        convert these strings to an int or double if necessary:

        int boolParms (Slewing, Tracking, Initialized, etc.)
        double RightAsc (Hours, JNow)
        double Declination (Degs, JNow)
        double ScopeAlititude (Degs)
        double ScopeAzimuth (Degs)
        double Secondary Axis Angle (Degs) (if a RotatorComms command, this will be
            the ParallacticAngle) (if this is a ReadScopeDestination command,
            it is the destination RA)
        double Primary Axis Angle (Degs) (if a RotatorComms command, this will be
            the ParallacticRate) (if this is a ReadScopeDestination command,
            it is the destination Dec)
        double ScopeSidereal Time (Hours) (if a RotatorComms command, this will be
            the CameraSolvedAngle) (if this is a ReadScopeDestination command,
            it is the destination ScopeAltitude)
        double Scope Julian Day  (if a RotatorComms command, this will be
            the Commanded Rotator GoTo position) (if this is a ReadScopeDestination
            command, it is the destination ScopeAzimuth)
        double Scope Time( Hours)
        double AirMass
        String "_" followed by message.

    The boolParms have bits in it that mean certain things as follows:

        Bit 00 (AND with    1) Scope Is Initialized
        Bit 01 (AND with    2) Scope Is Tracking (remains true when slewing)
        Bit 02 (AND with    4) Scope is Slewing
        Bit 03 (AND with    8) Scope is Parking
        Bit 04 (AND with   16) Scope is Parked
        Bit 05 (AND with   32) Scope is "Looking East" (GEM mount);
        Bit 06 (AND with   64) ServoController is in "Blinky" (Manual) mode,
                               one or both axis's
        Bit 07 (AND with  128) There is a communication fault between SiTechExe
                               and the ServoController
        Bit 08 (AND with  256) Limit Switch is activated (Primary Plus)
                               (ServoII and Brushless)
        Bit 09 (AND with  512) Limit Switch is activated (Primary Minus)
                               (ServoII and Brushless)
        Bit 10 (AND with 1024) Limit Switch is activated (Secondary Plus)
                               (ServoII and Brushless)
        Bit 11 (AND with 2048) Limit Switch is activated (Secondary Minus)
                               (ServoII and Brushless)
        Bit 12 (AND with 4096) Homing Switch Primary Axis is activated
        Bit 13 (AND with 8192) Homing Switch Secondary Axis is activated
        Bit 14 (AND with 16384) GoTo Commanded Rotator Position
                                (if this is a rotator response)
        Bit 15 (AND with 32768) Tracking at Offset Rate of some kind (non-sidereal)
        Bit 16 (AND with 65536) We are tracking a satellite now
        Bit 17 (AND with 131072) The tracking hasn't settled after a slew

    """

    items = status.strip().split(";")

    if (n_items := len(items)) != 12:
        raise ValueError(f"Invalid status: {status}. Expected 12 items, got {n_items}.")

    mask = ScopeStatusMaskbit(int(items[0]))

    return ScopeStatusDict(
        bool_params=int(items[0]),
        bool_params_labels=mask.name.split("|") if mask.name else [],
        right_ascension=float(items[1]),
        declination=float(items[2]),
        altitude=float(items[3]),
        azimuth=float(items[4]),
        secondary_axis_angle=float(items[5]),
        primary_axis_angle=float(items[6]),
        scope_sidereal_time=float(items[7]),
        scope_julian_day=float(items[8]),
        scope_time=float(items[9]),
        air_mass=float(items[10]),
    )
