import React from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { Menu, Container } from "semantic-ui-react";

const Header: React.FC = () => {
  const router = useRouter();
  const isActive: (pathname: string) => boolean = (pathname) =>
    router.pathname === pathname;

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
        </Container>
      </Menu>
    </nav>
  );
};

export default Header;
