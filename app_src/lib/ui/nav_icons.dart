import 'package:flutter/material.dart';

import 'duo_theme.dart';

/// Quattro destinazioni della barra inferiore, con icone Material standard.
enum NavMascotKind { photo, levels, learn, profile }

class NavMascotIcon extends StatelessWidget {
  final NavMascotKind kind;
  final double size;
  final Color scarf;
  final bool selected;

  const NavMascotIcon({
    super.key,
    required this.kind,
    required this.size,
    required this.scarf,
    this.selected = false,
  });

  IconData get icon => switch (kind) {
        NavMascotKind.photo => Icons.photo_camera_outlined,
        NavMascotKind.levels => Icons.grid_on,
        NavMascotKind.learn => Icons.school_outlined,
        NavMascotKind.profile => Icons.person_outline,
      };

  @override
  Widget build(BuildContext context) {
    final color = selected ? DuoColors.green : DuoColors.muted;
    return Icon(icon, size: size, color: color);
  }
}
