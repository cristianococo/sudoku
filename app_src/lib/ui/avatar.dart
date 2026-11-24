import 'package:flutter/material.dart';

import 'duo_theme.dart';

enum AvatarMood { idle, thinking, happy, error }

/// Icona di stato del tutor: solo icone Material standard.
class MoodIcon extends StatelessWidget {
  final AvatarMood mood;
  final double size;
  final Color scarfColor;
  final bool showShadow;

  const MoodIcon({
    super.key,
    this.mood = AvatarMood.idle,
    this.size = 72,
    this.scarfColor = DuoColors.yellow,
    this.showShadow = true,
  });

  IconData get icon => switch (mood) {
        AvatarMood.idle => Icons.grid_on,
        AvatarMood.thinking => Icons.lightbulb_outline,
        AvatarMood.happy => Icons.check_circle_outline,
        AvatarMood.error => Icons.error_outline,
      };

  Color get color => switch (mood) {
        AvatarMood.idle => DuoColors.blue,
        AvatarMood.thinking => DuoColors.yellowDark,
        AvatarMood.happy => DuoColors.green,
        AvatarMood.error => DuoColors.red,
      };

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(size * 0.28),
        border: Border.all(color: color, width: size * 0.045),
      ),
      child: Icon(icon, size: size * 0.54, color: color),
    );
  }
}

/// Nome storico usato dalla home: ora mostra un'icona di stato.
class TutorAvatar extends StatelessWidget {
  final AvatarMood mood;
  final double size;

  const TutorAvatar({super.key, required this.mood, this.size = 68});

  @override
  Widget build(BuildContext context) => MoodIcon(mood: mood, size: size);
}

/// Sequenza di tre icone usata nelle card: solo simboli Material.
class IconParade extends StatelessWidget {
  final double size;
  final List<Color>? scarves;

  const IconParade({super.key, required this.size, this.scarves});

  @override
  Widget build(BuildContext context) {
    final colors = scarves ?? [DuoColors.blue, DuoColors.green, DuoColors.yellow];
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        MoodIcon(size: size * 0.78, mood: AvatarMood.idle, scarfColor: colors[0]),
        SizedBox(width: size * 0.06),
        MoodIcon(size: size, mood: AvatarMood.happy, scarfColor: colors[1]),
        SizedBox(width: size * 0.06),
        MoodIcon(size: size * 0.78, mood: AvatarMood.idle, scarfColor: colors[2]),
      ],
    );
  }
}
