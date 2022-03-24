import React, { useState } from 'react'
import { Button, Form, Alert } from 'react-bootstrap';
import './LoginForm.css'

const LoginForm = ({ authenticate, resetPassword, onSuccess }) => {
  const [status, setStatus] = useState("idle")
  const [error, setError] = useState(null)

  const [user, setUser] = useState("")
  const [password, setPassword] = useState("")

  const submit = async() => {
    setError(null)
    setStatus("loading")
    try{
      const result = await authenticate({user, password})
      if(result.success){
        onSuccess(result)
        return
      }
      throw new Error()
    }catch(err){
      console.log("err", err)
      setError("Cannot authenticate")
      setStatus("error")
    }
  }

  const isValid = status !== "loading" && !!password

  return (
    <div id="container">
      <Form id="form" onSubmit={(e) => e.preventDefault}>
        <Form.Group>
          <Form.Label>Usuario</Form.Label>
          <Form.Control
            type="user"
            onChange={(e) => setUser(e.target.value)}
            value={user}
            placeholder="Usuario"
          />  
        </Form.Group>
        <br/>
        <Form.Group controlId="formBasicPassword">
          <Form.Label>Contraseña</Form.Label>
          <Form.Control
            type="password"
            onChange={(e) => setPassword(e.target.value)}
            value={password}
            placeholder="Contraseña"
          />
        </Form.Group>
        {error && <Alert variant="danger">{error}</Alert>}  
        <Button
          style={{ marginTop: 30 }}
          variant="primary"
          size="lg"
          block
          onClick={submit}
          type="submit"
          disable={!isValid}
        >
          Iniciar Sesi&oacute;n
        </Button>
        <Button
          style={{ marginTop: 30 }}
          variant="light"
          title="Recuperar contraseña"
          block
          size="sm"
          onClick={() => resetPassword(user)}
          type="button"
        >
          He olvidado mi contraseña  
        </Button>
      </Form>
    </div>
  )
}

export default LoginForm;