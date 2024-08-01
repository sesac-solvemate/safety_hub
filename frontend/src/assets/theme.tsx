// theme.ts
import { DefaultTheme } from 'styled-components';

// 테마 설정
const colors = {
  brand: '#027B8B',
  main: '#399AF9',
  text_default: '#1E1E1E',
  text_secondary: '#757575',
  text_tertiary: '#B3B3B3',
  btn_text: '#F5F5F5',
  btn_default: '#399AF9',
  btn_pressed: '#0078EE',
  btn_disabled: '#CECFD3',
  border_default: '#D9D9D9',
  bg: '#F7F7FC'
};


export type ColorsTypes = typeof colors;

const theme: DefaultTheme = {
  colors,
};

export default theme;
