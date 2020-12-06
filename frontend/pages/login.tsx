import Head from "next/head";
import LoginForm from "@/components/Auth/LoginForm";
import Link from "next/link";
import React from "react";
import styled from "styled-components";
import { GetServerSideProps } from "next";
import { ensureRedirectToData } from "@/utils.ts/ensure";
import Container from "@/components/UI/Container";
import AuthLayout from "@/components/Layout/AuthLayout";

interface ILogin {}

const Login = ({}: ILogin) => {
  return (
    <AuthLayout>
      <Wrapper>
        <Head>
          <title>Вход</title>
        </Head>
        <Container>
          <Inner>
            <Title>Войти в аккаунт</Title>
            <Main>
              <LoginForm />
            </Main>
            <Subtitle>Нет аккаунта?</Subtitle>
            <Bottom>
              <Link href="/register">
                <a>Регистрация</a>
              </Link>
            </Bottom>
          </Inner>
        </Container>
      </Wrapper>
    </AuthLayout>
  );
};

export default Login;

export const getServerSideProps: GetServerSideProps<ILogin> = async (ctx) => {
  ensureRedirectToData(ctx);
  return {
    props: {},
  };
};

const Wrapper = styled.div`
  background: url(login/login_bgc.png) no-repeat;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
  flex: 1;
  padding: 235px 0 110px;
`;

const Inner = styled.div`
  width: 100%;
  display: flex;
  align-items: center;
  flex-direction: column;
`;

const Title = styled.h1`
  font-family: "Play";
  font-weight: normal;
  font-size: 48px;
  line-height: 56px;
  color: ${({ theme }) => theme.white};
  margin-bottom: 84px;
`;
const Subtitle = styled.span`
  margin-top: 20px;
  font-family: "Play";
  font-style: normal;
  font-weight: normal;
  font-size: 18px;
  line-height: 21px;
  text-align: center;
  color: #ffffff;
`;

const Main = styled.span``;

const Bottom = styled.span`
  margin-top: 10px;
  font-family: "Play";
  font-style: normal;
  font-weight: normal;
  font-size: 18px;
  line-height: 21px;
  text-align: center;
  color: #ffffff;
`;
