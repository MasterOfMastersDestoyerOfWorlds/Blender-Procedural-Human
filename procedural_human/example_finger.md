Finger = (segment_lengths=[], radius_taper=0.85, curl_axis=Y):
    Segment = DualRadial(ik=IKLimits(x=(-10, 150), y=(-10, 10), z=(-5, 5)))
    segments = []
    norm_lengths = normalize(segment_lengths)
    radius = 1
    for i in range(len(segment_lengths)):
        seg = Segment(length=segment_lengths[i], radius=radius, profile_lookup=i) 
        segments.append(seg)
        radius = radius * radius_taper
    Nail = RadialAttachment(type=DualRadial, size_ratio=0.3, rotation=curl_axis) #id would be Index_Finger_Nail or Thumb_Finger_Nail
    Knuckle = Joint(type=QuadRadial, overlap=0.2) #optional profiles id that looks up by name otherwise use or create "Ring_Finger_Knuckle_Joint" profile curves
    AttachRaycast(last(segments), Nail)
    Extend(segments, axis=Z) #tells that the proximal joint is followed by the middle joint by the distal joint
    Join(segments, Knuckle) #inserts Finger joints between segments

Index = Finger([39.78, 22.38, 15.82])
Thumb = Finger([46.22, 21.67])
Middle = Finger([44.63, 26.33, 17.40])
Ring = Finger([41.37, 25.65, 17.30])
Little = Finger([32.74, 18.11, 15.96])