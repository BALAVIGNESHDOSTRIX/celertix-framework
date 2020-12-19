from celertix.tools.celertix_global import clx, Clxauth, ClxBlr,ClxRsp,ClxRegistry, clxuniv
from datetime import datetime, date


resusersaction = ClxBlr('res_users', url_prefix='/users')

@resusersaction.route('/user/create', methods=['POST'])
async def action_create_user(request):
     vals = {'name': request.form.get('name'), 'age': int(request.form.get('age'))}
     userobj = await clxuniv.env['res.user'].create(vals=vals)
     print(userobj._id, userobj.name, userobj.age)
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})


@resusersaction.route('/user/search', methods=['GET'])
async def action_search_user(request):
     name = request.args.get('name')
     age = request.args.get('age')
     userobj_l = await clxuniv.env['res.user'].search([('name', '=',name), '&', ('age', '=', age)])
     print(userobj_l._id)
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})


@resusersaction.route('/user/update', methods=['POST'])
async def action_search_user(request):
     name = request.form.get('name')
     age = request.form.get('age')
     print(name, age)
     userobj = await clxuniv.env['res.user'].search([('name', '=',name), '&', ('age', '=', age)])
     await userobj.write({'name': 'vignesh', 'age': 20})
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})

@resusersaction.route('/user/delete', methods=['POST'])
async def action_search_user(request):
     name = request.args.get('name')
     age = request.args.get('age')
     userobj = await clxuniv.env['res.user'].search([('name', '=',name), '&', ('age', '=', age)])
     for user in userobj:
          await user.unlink()
          break
     return SkyResponse.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})

@resusersaction.route('/user/timestamp', methods=['POST'])
async def action_timestamp_user(request):
     dt = datetime.now()
     userobj = await clxuniv.env['res.user'].create({'create_dt': dt})
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})


@resusersaction.route('/user/date', methods=['POST'])
async def action_date_user(request):
     dt = datetime.strftime(date.today(), '%Y-%m-%d')
     userobj = await clxuniv.env['res.user'].create({'write_dt': dt})
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})


@resusersaction.route('/user/salary', methods=['POST'])
async def action_salary_user(request):
     slry = 214.52
     userobj = await clxuniv.env['res.user'].create({'salary': slry})
     return ClxRsp.json({'msg': 'Success Token','res_code': 2000, 'result': 'good'})
     


ClxRegistry(resusersaction)
