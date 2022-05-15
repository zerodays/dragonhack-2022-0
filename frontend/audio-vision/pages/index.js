import { useEffect, useState } from 'react'
import { Container, Box, Toolbar, Typography } from '@mui/material';
import Image from 'next/image'
import useWebSocket from 'react-use-websocket';

const IP = 'ws://192.168.46.206:7000'

// const IP = 'wss://socketsbay.com/wss/v2/2/demo/'

const Home = () => {
  const [img, setImage] = useState()
  const [ang, setAngle] = useState()
  const [int, setIntensity] = useState()

  const {
    sendMessage,
  } = useWebSocket(IP, {
    onOpen: () => console.log('opened'),
    onMessage: (msg) => {
      const json = JSON.parse(msg.data)
      setImage(json.image)
      setAngle(json.angle)
      setIntensity(json.intesity)
      console.log(ang)
    },
    shouldReconnect: (closeEvent) => true,
  });

  useEffect(() => {
    console.log('useEffect')
    setInterval(() => {
      sendMessage('get')
    }, 500)
  }, [])

  return (
    <Box width="100%" height="100vh" position="relative">
      <Box p={2} position="static">
        <Toolbar sx={{ justifyContent: 'space-between' }}>
          {/* <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            News
          </Typography> */}
          <Box sx={{ flexGrow: 1 }} >
            <Box width="50px" height="50px">
              <Image
                src='/logo.png'
                layout={'fill'}
                objectFit={'contain'}
              />
            </Box>
          </Box>
          {/* <Button color="inherit">Login</Button> */}
        </Toolbar>
      </Box>
      <Container maxWidth="sm" sx={{ position: 'relative', height: 'calc(100% - 64px)' }}>
        <Box
          className="pointer"
          sx={{
            width: '700px',
            height: '700px',
            transform: `translate(-50%, -50%) rotate(${ang}rad)`,
            background: `radial-gradient(circle, rgba(0, 0, 0, 0.555) 0%, rgba(0, 212, 255, 0) ${int * 10}}%)`,
          }}>
          <Image
            src='/pointer_shadow.png'
            width='700px'
            height='700px'
          />
        </Box>
        <Box className="circle" sx={{ width: '500px', height: '500px', borderRadius: '50%' }}>
          {img ? (
            <img
              src={`data:image/jpeg;base64, ${img ?? 'mrs'}`}
              width='480px'
              height='480px'
              style={{ borderRadius: '50%', }}
            />) : (<Box className='plain-circle' width='480px' height='480px' >
              <Typography variant="h6" component="div" sx={{ textAlign: 'center', color: "white" }}>
                WAITING FOR CONNECTION
              </Typography>
            </Box>)
          }

        </Box>
        {/* <Typography variant="h6" component="div" sx={{ position: 'absolute', textAlign: 'center', color: "white", bottom: 40, right: 0, left: 0 }}>
          {conn}
        </Typography> */}
      </Container>
    </Box>
  )
}

export default Home;