import 'dotenv/config'
import { Request, Response } from 'express'
import { imageGeneratorService } from '../services/imageGeneratorService'
import { userService } from '../services/userService'

export const picturesController = {
  generate: async (req: Request, res: Response) => {
    const { authorization: auth } = req.headers
    const { type, description, count } = req.body

    console.log(req.body)

    if (!auth) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const token = (auth as string).split(' ')[1]
    console.log('token: ', token)

    const userId = userService.getUserByToken(token)

    if (!userId) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const credits = userService.getCredits(userId)

    if (credits.createLimit < count) {
      res.status(400).json({
        success: false,
        message: 'Not enough credits',
      })

      return
    }

    const promises = Array.from(Array(count)).map(async (x, i) => {
      const cur = await imageGeneratorService.generate(type, description)
      userService.useCredit(userId, 'create')
      return cur
    })

    const result = await Promise.all(promises)

    result.map((el) => {
      userService.addHistory(userId, 'create', el.image)
    })

    res.json({
      success: true,
      result,
    })
  },
  edit: async (req: Request, res: Response) => {
    const { authorization: auth } = req.headers
    const { image, description } = req.body

    if (!auth) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const token = (auth as string).split(' ')[1]
    const userId = userService.getUserByToken(token)
    if (!userId) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const credits = userService.getCredits(userId)
    if (credits.editLimit < 1) {
      res.status(400).json({
        success: false,
        message: 'Not enough credits',
      })

      return
    }

    const result = await imageGeneratorService.edit(image, description)

    userService.useCredit(userId, 'edit')
    userService.addHistory(userId, 'edit', result.image)

    res.json({
      success: true,
      result,
    })
  },
  history: (req: Request, res: Response) => {
    const { authorization: auth } = req.headers

    if (!auth) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const token = (auth as string).split(' ')[1]
    const userId = userService.getUserByToken(token)
    if (!userId) {
      res.status(401).json({
        success: false,
        message: 'Unauthorized',
      })

      return
    }

    const history = userService.getHistory(userId)

    res.json({
      success: true,
      history,
    })
  },
}
