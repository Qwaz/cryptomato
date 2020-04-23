import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Menu, Container, Button } from "semantic-ui-react";
import useUser from "../lib/useUser";

const Header: React.FC = () => {
  const { user, mutateUser } = useUser();

  const router = useRouter();
  const isActive: (pathname: string) => boolean = (pathname) =>
    router.pathname === pathname;

  const logout = async (e: React.SyntheticEvent) => {
    e.preventDefault();

    try {
      const res = await fetch(`http://localhost:3000/api/logout`);
      mutateUser();
    } catch (error) {
      console.error(error);
      alert(error);
    }
  };

  return (
    <nav>
      <Menu style={{ marginBottom: "6em" }}>
        <Container>
          <Menu.Item header>Cryptomato</Menu.Item>
          <Menu.Item active={isActive("/")}>
            <Link href="/">
              <a>Home</a>
            </Link>
          </Menu.Item>
          {user?.isLoggedIn && (
            <Menu.Menu position="right">
              <Menu.Item name="logout" onClick={logout} />
            </Menu.Menu>
          )}
        </Container>
      </Menu>
    </nav>
  );
};

export default Header;
