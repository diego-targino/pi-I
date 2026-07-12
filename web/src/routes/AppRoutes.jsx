import { Routes, Route } from "react-router-dom";

import Login from "../pages/Login/Login";
import Home from "../pages/Home/Home";
import EditarPerfil from "../pages/EditarPerfil/EditarPerfil";
import Historico from "../pages/Historico/Historico"; 
import Retorno from "../pages/Retorno/Retorno"; 
import Resultado from "../pages/Resultado/Resultado"; 
import Cadastrar from "../pages/Cadastro/Cadastrar";
import Propriedade from "../pages/Cadastro/Propriedade";
import Admin from "../pages/Admin/Admin";
import CadastroAdmin from "../pages/Admin/CadastroAdmin/CadastroAdmin"
import ListUsers from "../pages/Admin/ListUsers/ListUsers"

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      
      <Route path="/home" element={<Home />} />
      <Route path="/editar-perfil" element={<EditarPerfil />} />
      <Route path="/historico" element={<Historico />} />
      
      {/* CORRIGIDO: Agora o caminho bate exatamente com o seu botão de Login e com a URL */}
      <Route path="/cadastro" element={<Cadastrar />} />
      <Route path="/propriedade" element={<Propriedade />} />
      
      {/* ROTA DINÂMICA: Ajustada para usar a página Retorno */}
      <Route path="/retorno/:id" element={<Retorno />} />
      
      {/* ROTA DINÂMICA: Página de Resultado */}
      <Route path="/resultado/:id" element={<Resultado />} />

      <Route path="/admin" element={<Admin />} />
      <Route path="/cadastroAdmin" element={<CadastroAdmin />} />
      <Route path="/listUsers" element={<ListUsers />} />
    </Routes>
  );
}