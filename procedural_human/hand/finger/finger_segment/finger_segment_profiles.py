"""
Profile curve data for finger segments.

Each profile is a bezier curve normalized to 0-1 along the length,
with radius values as multipliers of the base segment radius.
"""

from enum import Enum


class ProfileType(Enum):
    """Types of profile curves"""

    X_PROFILE = "x_profile"
    Y_PROFILE = "y_profile"


class SegmentType(Enum):
    """Types of finger segments"""

    PROXIMAL = "proximal"
    MIDDLE = "middle"
    DISTAL = "distal"


DEFAULT_X_PROFILE_PROXIMAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.28606098890304565, -0.016038963571190834, 0.0005471110343933105),
            "handle_right": (-0.28606098890304565, 0.016038963571190834, -0.0005471110343933105),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (-0.33354711532592773, 0.0, 0.5),
            "handle_left": (0.0, 0.0, -0.19999998807907104),
            "handle_right": (0.0, 0.0, 0.19999998807907104),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (-0.28555792570114136, -0.02205190621316433, -0.007669806480407715),
            "handle_right": (0.28555795550346375, 0.02205190807580948, 0.007669806480407715),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}

DEFAULT_Y_PROFILE_PROXIMAL = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.0, -0.22212034463882446, -0.001552492380142212),
            "handle_right": (0.0, 0.22212034463882446, 0.001552492380142212),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.27149108052253723, 0.5),
            "handle_left": (0.0, 0.0, -0.19999998807907104),
            "handle_right": (0.0, 0.0, 0.19999998807907104),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.018338197842240334, 0.22059014439582825, 0.018535256385803223),
            "handle_right": (-0.01833820529282093, -0.22059021890163422, -0.018535256385803223),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}

DEFAULT_X_PROFILE_MIDDLE = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (0.2146512269973755, 0.04680848866701126, -0.02418816089630127),
            "handle_right": (-0.2146512269973755, -0.04680848866701126, 0.02418816089630127),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (-0.2507556676864624, -0.008383763022720814, 0.46616074442863464),
            "handle_left": (0.0, 0.0, -0.19999998807907104),
            "handle_right": (0.0, 0.0, 0.19999995827674866),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (-0.21704651415348053, 0.04107580706477165, 0.00740504264831543),
            "handle_right": (0.21704648435115814, -0.041075803339481354, -0.00740504264831543),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}

DEFAULT_Y_PROFILE_MIDDLE = {
    "points": [
        {
            "co": (0.0, 0.0, 0.0),
            "handle_left": (-0.032259587198495865, -0.22095711529254913, -0.011363670229911804),
            "handle_right": (0.032259587198495865, 0.22095711529254913, 0.011363670229911804),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.018781648948788643, 0.28789860010147095, 0.4947188198566437),
            "handle_left": (0.0, 0.0, -0.19999998807907104),
            "handle_right": (0.0, 0.0, 0.20000001788139343),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (-0.025025686249136925, 0.22101044654846191, 0.046151041984558105),
            "handle_right": (0.025025686249136925, -0.22101044654846191, -0.046151041984558105),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}

DEFAULT_X_PROFILE_DISTAL = {
    "points": [
        {
            "co": (0.0, -0.007444328628480434, 0.0),
            "handle_left": (0.22968104481697083, 0.0, -0.02658674120903015),
            "handle_right": (-0.11484050750732422, 0.0, 0.013293368741869926),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (-0.2694814205169678, 0.0033377287909388542, 0.0014964714646339417),
            "handle_left": (0.11538909375667572, -4.5027583837509155e-05, -0.0026405497919768095),
            "handle_right": (-0.11538910865783691, 4.5027583837509155e-05, 0.002640550024807453),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (-0.25984758138656616, 0.0022879978641867638, 0.4939092993736267),
            "handle_left": (0.0, 0.0, -0.07499998807907104),
            "handle_right": (0.0, 0.0, 0.1499999761581421),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, -0.007444328628480434, 1.0),
            "handle_left": (-0.21021553874015808, 0.0, 0.028403639793395996),
            "handle_right": (0.21021553874015808, 0.0, -0.028403639793395996),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}

DEFAULT_Y_PROFILE_DISTAL = {
    "points": [
        {
            "co": (0.010026626288890839, -0.00872201006859541, 0.0077520702034235),
            "handle_left": (0.0, -0.23969565331935883, -0.016991382464766502),
            "handle_right": (0.0, 0.11984781175851822, 0.008495690301060677),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.03451903164386749, 0.31967273354530334, 0.0),
            "handle_left": (0.01063016802072525, -0.11887684464454651, -0.005378386937081814),
            "handle_right": (-0.010630171746015549, 0.1188768744468689, 0.005378388334065676),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.03075970523059368, 0.2767794728279114, 0.521970272064209),
            "handle_left": (0.0, 0.00013309717178344727, -0.07410600781440735),
            "handle_right": (0.0, -0.0003152787685394287, 0.17553937435150146),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        },
        {
            "co": (0.0, 0.0, 1.0),
            "handle_left": (0.02283559925854206, 0.22929370403289795, 0.04811358451843262),
            "handle_right": (-0.021612584590911865, -0.21701334416866302, -0.04553675651550293),
            "handle_left_type": "ALIGNED",
            "handle_right_type": "ALIGNED",
        }
    ]
}


PROFILE_DATA = {
    SegmentType.PROXIMAL: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_PROXIMAL,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_PROXIMAL,
    },
    SegmentType.MIDDLE: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_MIDDLE,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_MIDDLE,
    },
    SegmentType.DISTAL: {
        ProfileType.X_PROFILE: DEFAULT_X_PROFILE_DISTAL,
        ProfileType.Y_PROFILE: DEFAULT_Y_PROFILE_DISTAL,
    },
}


def get_profile_data(segment_type: SegmentType, profile_type: ProfileType):
    """
    Get profile data for a given segment and profile type.

    Args:
        segment_type: SegmentType enum
        profile_type: ProfileType enum

    Returns:
        Profile data dictionary
    """

    return PROFILE_DATA[segment_type][profile_type]


__all__ = [
    "ProfileType",
    "SegmentType",
    "PROFILE_DATA",
    "get_profile_data",
    "DEFAULT_X_PROFILE_PROXIMAL",
    "DEFAULT_Y_PROFILE_PROXIMAL",
    "DEFAULT_X_PROFILE_MIDDLE",
    "DEFAULT_Y_PROFILE_MIDDLE",
    "DEFAULT_X_PROFILE_DISTAL",
    "DEFAULT_Y_PROFILE_DISTAL",
]
