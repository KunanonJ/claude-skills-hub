# Expo Course Map

Use this reference when a user asks to learn from Expo courses or turn Expo learning resources into project tasks.

## Source Pages

- Expo Learn: https://expo.dev/learn
- Expo tutorial: https://docs.expo.dev/tutorial/introduction/
- Expo Router: https://docs.expo.dev/router/introduction/
- Development builds: https://docs.expo.dev/develop/development-builds/introduction/
- EAS Build: https://docs.expo.dev/build/introduction/
- EAS Update: https://docs.expo.dev/eas-update/introduction/
- Expo Skills: https://docs.expo.dev/skills/

## Expo Learn Resource Categories

- Courses: React Native animations, beginner React Native, Expo Router, gestures, intermediate React Native, notJust.dev, Galaxies.dev, Code with Beto, freeCodeCamp, Frontend Masters.
- YouTube channels: notJust.dev, Code with Beto, Simon Grimm, Catalin Miron, Reactiive.
- Expo team talks: Expo Router, development builds, EAS, updates, debugging, native capabilities, desktop, Linux, V8, and platform workflow talks.
- Podcasts: React Universe on Air and React Native Radio.

## Course Lane Routing

| User intent | Course lane | Use next |
| --- | --- | --- |
| "Teach me Expo from zero" | Beginner universal app | `expo-course-to-production`, then `building-native-ui` |
| "Turn my web app into iOS/Android" | Web-to-mobile architecture | `expo-course-to-production`, `react-native-expert`, `use-dom` if reusing web UI |
| "Build app screens and navigation" | Router/UI | `building-native-ui`, `react-native-expert` |
| "Add API/data fetching" | Data/API | `native-data-fetching`, `expo-api-routes` |
| "Use camera, notifications, Firebase, native SDKs" | Native capability | `expo-dev-client`, `expo-module` if custom native code is required |
| "Ship to TestFlight/Play Store" | Release | `expo-deployment` |
| "Automate mobile CI/CD" | Operations | `expo-cicd-workflows`, `advanced-automation-architect` |
| "Upgrade Expo SDK" | Maintenance | `upgrading-expo` |

## Verification Commands

Prefer commands already present in the project. If absent, use these as candidates:

```bash
npx expo doctor
npm test
npx expo start --web
npx expo start --ios
npx expo start --android
npx eas-cli@latest build:configure
npx eas-cli@latest build --platform all --profile preview --non-interactive
```

Do not run cloud builds, submit commands, or update publishing commands without explicit user approval.
