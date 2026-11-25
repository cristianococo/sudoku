import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:http/testing.dart';

import '../lib/core/api_service.dart';
import '../lib/core/app_prefs.dart';

void main() {
  test('ApiService invia apikey e token di sessione alla Edge Function', () async {
    final client = MockClient((request) async {
      expect(request.headers['apikey'], 'anon-key');
      expect(request.headers['authorization'], 'Bearer session-token');
      expect(
        request.url.path,
        '/functions/v1/gemini-proxy/api/status',
      );
      return http.Response(
        '{"configured":true,"model":"gemini-3.6-flash","runtime":"supabase-edge-function"}',
        200,
      );
    });

    final api = ApiService(
      'https://demo.supabase.co/functions/v1/gemini-proxy',
      apiKey: 'anon-key',
      client: client,
      tokenProvider: () async => 'session-token',
    );

    final status = await api.status();
    expect(status.configured, isTrue);
    expect(status.model, 'gemini-3.6-flash');
  });

  test('Senza token di sessione ApiService usa la chiave pubblica', () async {
    final client = MockClient((request) async {
      expect(request.headers['authorization'], 'Bearer anon-key');
      return http.Response(
        '{"configured":true,"model":"gemini-3.6-flash"}',
        200,
      );
    });
    final api = ApiService(
      'https://demo.supabase.co/functions/v1/gemini-proxy',
      apiKey: 'anon-key',
      client: client,
    );
    expect((await api.status()).configured, isTrue);
  });

  test('AppPrefs deriva la URL della funzione dal progetto Supabase', () {
    expect(
      AppPrefs.functionsUrl('https://demo.supabase.co/'),
      'https://demo.supabase.co/functions/v1/gemini-proxy',
    );
    expect(
      AppPrefs.functionsUrl('https://demo.supabase.co'),
      'https://demo.supabase.co/functions/v1/gemini-proxy',
    );
  });
}
