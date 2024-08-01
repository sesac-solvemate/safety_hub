import React from "react";
import "./assets/fonts/Font.css";
import ReactDOM from "react-dom/client";
import App from "./App";
import { createGlobalStyle, ThemeProvider } from "styled-components";
import theme from "./assets/theme";

const GlobalStyle = createGlobalStyle`
  html {
    font-size: 16px; /* 기본 폰트 크기를 설정합니다. 필요에 따라 조정 가능합니다. */
  }
  body {
    margin: 0;
    font-family: 'NotoSansKR-Medium', sans-serif;
  }
`;

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);

root.render(
  <ThemeProvider theme={theme}>
    <GlobalStyle />
    <App />
  </ThemeProvider>
);
